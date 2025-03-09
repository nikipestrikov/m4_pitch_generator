import layout
from pdfworker import process_developer_pdf
import os
import sys

csv_file_path = os.path.join(os.path.dirname(__file__), "Unit_Availability.csv")

# Make sure csv_parser.py is in the same directory
try:
    import csv_parser
except ImportError:
    print("Warning: csv_parser.py module not found. Using built-in fallback implementation.")


    # Define minimal fallback implementation of csv_parser
    class csv_parser:
        @staticmethod
        def get_project_data(csv_path, project_name=None):
            """Fallback implementation that returns default data"""
            description_lines = [
                "CSV parser module not found. This is placeholder content.",
                "Please ensure csv_parser.py is in the same directory as this script.",
                "This property offers an exceptional investment opportunity with modern amenities",
                "and attractive returns in a prime location."
            ]

            available_units = [
                {
                    "unit_id": "A101",
                    "size": "1,250",
                    "price": "$750,000",
                    "bedrooms": 2,
                    "bathrooms": 2,
                    "features": "Corner unit with balcony"
                },
                {
                    "unit_id": "B205",
                    "size": "1,800",
                    "price": "$1,050,000",
                    "bedrooms": 3,
                    "bathrooms": 2.5,
                    "features": "Penthouse with city view"
                }
            ]

            project_info = {
                'name': 'Default Project',
                'developer': 'Default Developer',
                'location': {'url': ''}
            }

            return description_lines, available_units, project_info

        @staticmethod
        def list_projects_in_csv(csv_path):
            """Fallback implementation that returns a default project"""
            return [{
                'name': 'Default Project',
                'developer': 'Default Developer',
                'unit_count': 2,
                'location_url': ''
            }]

def create_pitch_deck(output_filename, header_image_path, developer_pdf=None, csv_path=None,
                      project_name=None, title="Investment Opportunity", description_lines=None):
    """
    Creates a one-page pitch deck PDF with property details and description.
    """
    # Initialize with default description if none provided
    if not description_lines:
        description_lines = [
            "This premium investment property offers an exceptional opportunity in the heart of the city's",
            "most vibrant district. Recently renovated with high-end finishes, the property features modern",
            "amenities, energy-efficient systems, and a versatile floor plan suitable for various commercial",
            "purposes. With strong tenant demand in the area and projected growth, this investment promises",
            "consistent returns and appreciation potential."
        ]

    # Get available units from CSV if provided
    if csv_path and os.path.exists(csv_path):
        try:
            # Extract only the units from the CSV
            available_units = csv_parser.get_units_from_csv(csv_path)
            if not available_units:
                # Fall back to default content if no units found
                _, available_units = default_content()

            print(f"Extracted {len(available_units)} units from CSV")

        except Exception as e:
            print(f"Error reading CSV file: {e}")
            # Fall back to default content
            _, available_units = default_content()
    elif developer_pdf and os.path.exists(developer_pdf):
        # Fall back to PDF processing if CSV is not provided
        try:
            desc_lines, available_units = process_developer_pdf(developer_pdf)
            # Only use the units, not the description from PDF
        except Exception as e:
            print(f"Error processing PDF: {e}")
            # Fall back to default content
            _, available_units = default_content()
    else:
        # Default content if neither CSV nor PDF is provided
        _, available_units = default_content()

    # Initialize the PDF with our layout
    c, width, height, header_height, content_start_y = layout.initialize_pdf_layout(
        output_filename, header_image_path, title
    )

    # ============ DESCRIPTION SECTION ============
    section_y = content_start_y  # Start position for the first section

    # Add Description section header
    c.setFillColor(layout.PRIMARY_COLOR)
    c.setFont("Helvetica", 12)
    c.drawString(50, section_y, "Property Description:")

    # Add the description paragraph
    c.setFillColor(layout.TEXT_COLOR)
    c.setFont("Helvetica", 10)
    line_height = 15  # spacing between lines
    for i, line in enumerate(description_lines):
        c.drawString(70, section_y - 20 - (i * line_height), line)

    # ============ AVAILABLE UNITS SECTION ============
    # Calculate the Y position for the units section (below description)
    units_y = section_y - 30 - (len(description_lines) * line_height)

    # Add Available Units section header
    c.setFillColor(layout.PRIMARY_COLOR)
    c.setFont("Helvetica", 12)
    c.drawString(50, units_y, "Available Units:")

    # Table setup - centered on page with borders
    table_width = 500  # Total width of the table
    left_margin = (width - table_width) / 2  # Center the table horizontally

    # Define column positions and widths for the table (relative to left margin)
    col_widths = {
        'id': 40,
        'floor': 30,
        'bed': 25,
        'area': 45,
        'total': 45,
        'price': 50,
        'tax': 50,
        'total_cost': 50,
        'price_m2': 50,
        'rent': 50,
        'roi': 65  # Increased from 25 to provide more space
    }

    # Calculate and adjust the total width to match the defined table_width
    total_col_width = sum(col_widths.values())
    if total_col_width != table_width:
        # Adjust each column width proportionally to match the table_width
        ratio = table_width / total_col_width
        col_widths = {key: int(width * ratio) for key, width in col_widths.items()}
        # Ensure the sum equals table_width (account for rounding)
        adjustment = table_width - sum(col_widths.values())
        col_widths['roi'] += adjustment  # Add any rounding difference to the last column

    # Calculate absolute positions of columns
    cols = {}
    current_pos = left_margin
    for key, width in col_widths.items():
        cols[key] = current_pos
        current_pos += width

    # Table positioning and measurements
    header_y = units_y - 25  # Adjusted down to add space after section title
    row_height = 20  # Increased row height to prevent overlap

    # Draw table outline
    table_rows = min(8, len(available_units) + 1)  # Header + data rows (max 7 data rows)
    table_height = row_height * table_rows

    # Draw outer border of table
    c.setStrokeColor(layout.SECONDARY_COLOR)
    c.rect(left_margin, header_y - table_height, table_width, table_height)

    # Draw header row background
    c.setFillColor(layout.SECONDARY_COLOR.clone(alpha=0.2))  # Light background color
    c.rect(left_margin, header_y - row_height, table_width, row_height, fill=1, stroke=0)

    # Draw header row border
    c.setStrokeColor(layout.SECONDARY_COLOR)
    c.line(left_margin, header_y - row_height, left_margin + table_width, header_y - row_height)

    # Draw vertical lines for columns
    current_x = left_margin
    for i, width in enumerate(col_widths.values()):
        if i > 0:  # Skip the leftmost edge since it's part of the rectangle
            c.line(current_x, header_y, current_x, header_y - table_height)
        current_x += width

    # Function to perfectly center text both horizontally and vertically in a cell
    def draw_centered_text(c, x, width, y_top, y_bottom, text, is_header=False):
        # Select font based on whether it's a header or not
        font_name = "Helvetica-Bold" if is_header else "Helvetica"
        font_size = 7

        # Set the font for proper text width calculation
        c.setFont(font_name, font_size)

        # Calculate horizontal center position
        text_width = c.stringWidth(text, font_name, font_size)
        centered_x = x + (width - text_width) / 2

        # Calculate vertical center position
        cell_height = y_top - y_bottom
        text_height = font_size  # Approximate text height
        centered_y = y_bottom + (cell_height - text_height) / 2 + text_height * 0.3  # Adjust for visual center

        # Draw the text
        c.drawString(centered_x, centered_y, text)

    # Draw table headers (centered vertically and horizontally)
    c.setFillColor(layout.PRIMARY_COLOR)
    c.setFont("Helvetica-Bold", 7)

    # Draw headers with perfect centering
    header_top = header_y
    header_bottom = header_y - row_height
    draw_centered_text(c, cols['id'], col_widths['id'], header_top, header_bottom, "Unit ID", True)
    draw_centered_text(c, cols['floor'], col_widths['floor'], header_top, header_bottom, "Floor", True)
    draw_centered_text(c, cols['bed'], col_widths['bed'], header_top, header_bottom, "Bed", True)
    draw_centered_text(c, cols['area'], col_widths['area'], header_top, header_bottom, "Int. Area", True)
    draw_centered_text(c, cols['total'], col_widths['total'], header_top, header_bottom, "Total Area", True)
    draw_centered_text(c, cols['price'], col_widths['price'], header_top, header_bottom, "Price", True)
    draw_centered_text(c, cols['tax'], col_widths['tax'], header_top, header_bottom, "VAT/Transfer", True)
    draw_centered_text(c, cols['total_cost'], col_widths['total_cost'], header_top, header_bottom, "Total Cost", True)
    draw_centered_text(c, cols['price_m2'], col_widths['price_m2'], header_top, header_bottom, "Price/m²", True)
    draw_centered_text(c, cols['rent'], col_widths['rent'], header_top, header_bottom, "Rental Rate", True)
    draw_centered_text(c, cols['roi'], col_widths['roi'], header_top, header_bottom, "ROI", True)

    # Add horizontal lines between rows
    for i in range(1, min(8, len(available_units) + 1)):
        row_y = header_y - (i * row_height)
        c.line(left_margin, row_y, left_margin + table_width, row_y)

    # Add units data with perfect centering in each cell
    c.setFillColor(layout.TEXT_COLOR)
    c.setFont("Helvetica", 7)

    for i, unit in enumerate(available_units[:7]):  # Limit to 7 units to fit in page
        if i >= 7:  # Safety check
            break

        # Calculate row top and bottom positions for vertical centering
        row_top = header_y - (i + 1) * row_height
        row_bottom = header_y - (i + 2) * row_height

        # Draw each column value perfectly centered in its cell
        unit_id = str(unit.get("unit_id", ""))
        draw_centered_text(c, cols['id'], col_widths['id'], row_top, row_bottom, unit_id)

        floor = str(unit.get("floor", ""))
        draw_centered_text(c, cols['floor'], col_widths['floor'], row_top, row_bottom, floor)

        bedrooms = str(unit.get("bedrooms", ""))
        draw_centered_text(c, cols['bed'], col_widths['bed'], row_top, row_bottom, bedrooms)

        # Format areas with m² units
        internal_area = unit.get("internal_area", "")
        if internal_area:
            internal_area = f"{internal_area} m²"
        draw_centered_text(c, cols['area'], col_widths['area'], row_top, row_bottom, internal_area)

        total_covered = unit.get("total_covered", "")
        if total_covered:
            total_covered = f"{total_covered} m²"
        draw_centered_text(c, cols['total'], col_widths['total'], row_top, row_bottom, total_covered)

        # Price and financial information
        asking_price = str(unit.get("asking_price", ""))
        draw_centered_text(c, cols['price'], col_widths['price'], row_top, row_bottom, asking_price)

        # VAT or Transfer Fee - display only the value
        tax_value = str(unit.get("tax_value", ""))
        draw_centered_text(c, cols['tax'], col_widths['tax'], row_top, row_bottom, tax_value)

        # Total Cost
        total_cost = str(unit.get("total_cost", ""))
        draw_centered_text(c, cols['total_cost'], col_widths['total_cost'], row_top, row_bottom, total_cost)

        # Price per m²
        price_per_m2 = str(unit.get("price_per_m2", ""))
        draw_centered_text(c, cols['price_m2'], col_widths['price_m2'], row_top, row_bottom, price_per_m2)

        # Rental Rate
        rental_rate = str(unit.get("rental_rate", ""))
        draw_centered_text(c, cols['rent'], col_widths['rent'], row_top, row_bottom, rental_rate)

        # ROI
        roi = str(unit.get("roi", ""))
        draw_centered_text(c, cols['roi'], col_widths['roi'], row_top, row_bottom, roi)

    # Save the PDF
    c.save()

    print(f"PDF created successfully: {output_filename}")




def default_content():
    """Provides default content when CSV or PDF parsing fails"""
    description_lines = [
        "This premium investment property offers an exceptional opportunity in the heart of the city's",
        "most vibrant district. Recently renovated with high-end finishes, the property features modern",
        "amenities, energy-efficient systems, and a versatile floor plan suitable for various commercial",
        "purposes. With strong tenant demand in the area and projected growth, this investment promises",
        "consistent returns and appreciation potential."
    ]

    available_units = [
        {
            "unit_id": "A101",
            "size": "1,250",
            "price": "$750,000",
            "bedrooms": 2,
            "bathrooms": 2,
            "features": "Corner unit with balcony"
        },
        {
            "unit_id": "B205",
            "size": "1,800",
            "price": "$1,050,000",
            "bedrooms": 3,
            "bathrooms": 2.5,
            "features": "Penthouse with city view"
        },
        {
            "unit_id": "C103",
            "size": "950",
            "price": "$580,000",
            "bedrooms": 1,
            "bathrooms": 1,
            "features": "Studio with modern kitchen"
        }
    ]

    return description_lines, available_units


if __name__ == "__main__":
    # Example usage with CSV
    csv_path = "Unit_Availability.csv"

    if os.path.exists(csv_path):
        try:
            # Generate pitch deck using units from CSV but with default description and title
            create_pitch_deck(
                output_filename="pitch_deck_from_csv.pdf",
                header_image_path="header_image.jpg",
                csv_path=csv_path,
                title="Premium Investment Property"  # Use default title
            )
        except Exception as e:
            print(f"Error processing CSV file: {e}")
            # Fall back to default
            create_pitch_deck(
                output_filename="pitch_deck_example.pdf",
                header_image_path="header_image.jpg"
            )
    else:
        print(f"CSV file not found at {csv_path}. Using default content.")
        # Fall back to original example with optional PDF
        create_pitch_deck(
            output_filename="pitch_deck_example.pdf",
            header_image_path="header_image.jpg",
            developer_pdf="developer_brochure.pdf",  # This is optional
            title="Premium Investment Property"
        )
