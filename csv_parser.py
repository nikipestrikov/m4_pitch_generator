import csv
import os
from typing import Dict, List

def extract_units_from_csv(csv_path: str) -> List[Dict]:
    """
    Extract unit information from a CSV file.

    Extracts the following fields for each unit:
    - Unit ID
    - Floor
    - Bedrooms (extracted from Typology)
    - Internal Area
    - Covered Veranda (labeled as 'Covered Area' in CSV)
    - Total Covered Area
    - Asking Price
    - VAT
    - Transfer Fee
    - Rental Rate
    - Additional calculated fields: Total Cost, Price/m², ROI
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    available_units = []

    try:
        # Read the CSV file with utf-8-sig encoding to handle BOM character
        with open(csv_path, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)

            if not reader.fieldnames:
                raise ValueError("CSV file appears to be empty or has no headers")

            # Process each row
            for row in reader:
                # Parse bedroom count from typology (e.g., "2 bedrooms" -> 2)
                bedroom_count = ''
                typology = row.get('Typology', '')
                if typology and len(typology) > 0 and typology[0].isdigit():
                    bedroom_count = typology[0]

                # Extract tax information (VAT and Transfer Fee)
                vat_str = row.get('VAT', '').strip()
                transfer_fee_str = row.get('Transfer Fee', '').strip()

                # Clean and convert tax values to numeric for comparison
                vat_value = 0
                transfer_fee_value = 0

                try:
                    vat_value = float(''.join(c for c in vat_str if c.isdigit() or c == '.')) if vat_str else 0
                except ValueError:
                    vat_value = 0

                try:
                    transfer_fee_value = float(
                        ''.join(c for c in transfer_fee_str if c.isdigit() or c == '.')) if transfer_fee_str else 0
                except ValueError:
                    transfer_fee_value = 0

                # Determine which tax to display based on non-zero value
                # Priority: VAT first if both have values
                if vat_value > 0:
                    tax_type = "VAT"
                    tax_value = vat_str
                    tax_amount = vat_value
                elif transfer_fee_value > 0:
                    tax_type = "Transfer Fee"
                    tax_value = transfer_fee_str
                    tax_amount = transfer_fee_value
                else:
                    tax_type = ""
                    tax_value = ""
                    tax_amount = 0

                # Extract asking price and total covered area for calculations
                asking_price_str = row.get('Asking Price', '0')
                total_covered_str = row.get('Total Covered Area', '0')
                rental_rate = row.get('Rental Rate', '')

                # Calculate derived values
                try:
                    # Remove currency symbols and commas for calculation
                    asking_price = float(''.join(c for c in asking_price_str if c.isdigit() or c == '.'))
                    total_covered = float(''.join(c for c in total_covered_str if c.isdigit() or c == '.'))

                    # Calculate price per square meter
                    price_per_m2 = asking_price / total_covered if total_covered > 0 else 0

                    # Calculate total cost (asking price + tax)
                    total_cost = asking_price + tax_amount

                    # Calculate ROI if rental rate is available
                    roi = 0
                    if rental_rate:
                        annual_rental = float(''.join(c for c in rental_rate if c.isdigit() or c == '.')) * 12
                        roi = (annual_rental / asking_price) * 100 if asking_price > 0 else 0

                except (ValueError, ZeroDivisionError):
                    price_per_m2 = 0
                    total_cost = 0
                    roi = 0

                # Store the unit information
                unit = {
                    'unit_id': row.get('Unit ID', ''),
                    'floor': row.get('Floor', ''),
                    'bedrooms': bedroom_count,
                    'internal_area': row.get('Internal Area', ''),
                    'total_covered': row.get('Total Covered Area', ''),
                    'asking_price': row.get('Asking Price', ''),
                    'tax_type': tax_type,
                    'tax_value': tax_value,
                    'total_cost': f"{total_cost:,.0f}" if total_cost > 0 else '',
                    'price_per_m2': f"{price_per_m2:,.0f}" if price_per_m2 > 0 else '',
                    'rental_rate': rental_rate,
                    'roi': f"{roi:.1f}%" if roi > 0 else ''
                }

                available_units.append(unit)

        return available_units
    except Exception as e:
        print(f"Error parsing CSV file: {e}")
        return []

def get_units_from_csv(csv_path: str) -> List[Dict]:
    """
    Get available units from the CSV file.
    """
    return extract_units_from_csv(csv_path)
