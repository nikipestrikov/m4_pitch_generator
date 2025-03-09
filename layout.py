import layout


def create_pitch_deck(output_filename, header_image_path, title="Investment Opportunity"):
    """
    Creates a one-page pitch deck PDF with property details.

    Args:
        output_filename (str): Path where to save the PDF
        header_image_path (str): Path to the header image
        title (str): Title for the pitch deck
    """
    # Initialize the PDF with our layout
    c, width, height, header_height, content_start_y = layout.initialize_pdf_layout(
        output_filename, header_image_path, title
    )

    # Add section header with primary color
    c.setFillColor(layout.PRIMARY_COLOR)
    c.setFont("Helvetica", 12)
    c.drawString(50, content_start_y, "Property Details:")

    # Placeholder for property details with text color
    c.setFillColor(layout.TEXT_COLOR)
    c.setFont("Helvetica", 10)
    c.drawString(70, content_start_y - 20, "• Location: Premium Downtown")
    c.drawString(70, content_start_y - 35, "• Size: 2,500 sq ft")
    c.drawString(70, content_start_y - 50, "• Price: $1,200,000")
    c.drawString(70, content_start_y - 65, "• ROI: 12% annually")

    # Save the PDF
    c.save()

    print(f"PDF created successfully: {output_filename}")


if __name__ == "__main__":
    # Example usage
    create_pitch_deck(
        "pitch_deck_example.pdf",
        "header_image.jpg",
        "Premium Investment Property"
    )
