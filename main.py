import layout
from pdfworker import process_developer_pdf
import os


def create_pitch_deck(output_filename, header_image_path, developer_pdf=None, title="Investment Opportunity"):
    """
    Creates a one-page pitch deck PDF with property details and description.

    Args:
        output_filename (str): Path where to save the PDF
        header_image_path (str): Path to the header image
        developer_pdf (str): Path to developer's PDF (optional)
        title (str): Title for the pitch deck
    """
    # Process developer PDF if provided
    if developer_pdf and os.path.exists(developer_pdf):
        description_lines, available_units = process_developer_pdf(developer_pdf)
    else:
        # Default content if no PDF is provided
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

    # Add table headers
    c.setFillColor(layout.SECONDARY_COLOR)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(70, units_y - 20, "Unit")
    c.drawString(130, units_y - 20, "Size (sq ft)")
    c.drawString(210, units_y - 20, "Price")
    c.drawString(280, units_y - 20, "Bedrooms")
    c.drawString(350, units_y - 20, "Features")

    # Add units data
    c.setFillColor(layout.TEXT_COLOR)
    c.setFont("Helvetica", 9)
    for i, unit in enumerate(available_units[:5]):  # Limit to 5 units to fit on page
        y_pos = units_y - 40 - (i * 15)
        c.drawString(70, y_pos, unit.get("unit_id", ""))
        c.drawString(130, y_pos, unit.get("size", ""))
        c.drawString(210, y_pos, unit.get("price", ""))
        c.drawString(280, y_pos, f"{unit.get('bedrooms', '')} BR / {unit.get('bathrooms', '')} BA")

        # Truncate features if too long
        features = unit.get("features", "")
        if len(features) > 25:
            features = features[:22] + "..."
        c.drawString(350, y_pos, features)

    # ============ PROPERTY DETAILS SECTION ============
    # Calculate the Y position for the details section (below available units)
    details_y = units_y - 40 - (min(len(available_units), 5) * 15) - 30

    # Add section header with primary color
    c.setFillColor(layout.PRIMARY_COLOR)
    c.setFont("Helvetica", 12)
    c.drawString(50, details_y, "Property Details:")

    # Placeholder for property details with text color
    c.setFillColor(layout.TEXT_COLOR)
    c.setFont("Helvetica", 10)
    c.drawString(70, details_y - 20, "• Location: Premium Downtown")
    c.drawString(70, details_y - 35, "• Size: 2,500 sq ft")
    c.drawString(70, details_y - 50, "• Price: $1,200,000")
    c.drawString(70, details_y - 65, "• ROI: 12% annually")

    # Save the PDF
    c.save()

    print(f"PDF created successfully: {output_filename}")


if __name__ == "__main__":
    # Example usage
    create_pitch_deck(
        "pitch_deck_example.pdf",
        "header_image.jpg",
        "developer_brochure.pdf",  # This is optional - if the file exists, content will be extracted
        "Premium Investment Property"
    )
