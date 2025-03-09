from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from PIL import Image
import os


def create_pitch_deck(output_filename, header_image_path, title="Investment Opportunity"):
    """
    Creates a one-page pitch deck PDF with a header image.

    Args:
        output_filename (str): Path where to save the PDF.
        header_image_path (str): Path to the header image.
        title (str): Title for the pitch deck.
    """
    # Define company colors
    primary_color = HexColor('#186685')  # Dark blue
    secondary_color = HexColor('#50adc9')  # Light blue
    background_color = HexColor('#e2ecf4')  # Light background
    text_color = HexColor('#186685')  # Using primary color for text
    white = HexColor('#ffffff')  # White

    # Define page dimensions (letter size)
    width, height = letter

    # Create a new PDF with ReportLab
    c = canvas.Canvas(output_filename, pagesize=letter)

    # Fill page with background color
    c.setFillColor(white)
    c.rect(0, 0, width, height, fill=True)

    # Calculate header area (top 15% of page)
    header_height = height * 0.15

    # Process and place the header image
    if os.path.exists(header_image_path):
        # Open image
        img = Image.open(header_image_path)
        img_width, img_height = img.size

        # Calculate dimensions for cropping
        # We want to keep the image width-to-height ratio equal to the header area's ratio
        target_ratio = width / header_height

        if img_width / img_height > target_ratio:  # Image is wider than needed
            # Calculate new height to maintain aspect ratio
            crop_height = img_height
            crop_width = crop_height * target_ratio

            # Center the crop horizontally
            left = (img_width - crop_width) / 2
            right = left + crop_width

            # Crop the image
            img_cropped = img.crop((left, 0, right, crop_height))
        else:  # Image is taller than needed
            # Calculate new width to maintain aspect ratio
            crop_width = img_width
            crop_height = crop_width / target_ratio

            # Center the crop vertically - take from the middle of the image
            top = (img_height - crop_height) / 2
            bottom = top + crop_height

            # Crop the image
            img_cropped = img.crop((0, top, crop_width, bottom))

        # Save the processed image temporarily
        temp_image_path = "temp_header.jpg"
        img_cropped.save(temp_image_path, quality=95)  # High quality

        # Place the image at the top of the page, full width
        c.drawImage(temp_image_path, 0, height - header_height, width=width, height=header_height)

        # Clean up temporary file
        os.remove(temp_image_path)

    # Add title below the header area
    c.setFillColor(primary_color)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - header_height - 40, title)

    # Add section header with primary color
    c.setFillColor(primary_color)
    c.setFont("Helvetica", 12)
    c.drawString(50, height - header_height - 80, "Property Details:")

    # Placeholder for property details with text color
    c.setFillColor(text_color)
    c.setFont("Helvetica", 10)
    c.drawString(70, height - header_height - 100, "• Location: Premium Downtown")
    c.drawString(70, height - header_height - 115, "• Size: 2,500 sq ft")
    c.drawString(70, height - header_height - 130, "• Price: $1,200,000")
    c.drawString(70, height - header_height - 145, "• ROI: 12% annually")

    def add_company_footer(c, width, height, primary_color, secondary_color):
        """
        Adds a professional footer with company contact details to the PDF.

        Args:
            c: ReportLab canvas object
            width: Page width
            height: Page height
            primary_color: Company primary color
            secondary_color: Company secondary color
        """
        # Footer positioning
        footer_height = 40
        footer_top = footer_height
        margin = 50

        # Add subtle separator line
        c.setStrokeColor(secondary_color)
        c.setLineWidth(0.75)
        c.line(margin, footer_top + 10, width - margin, footer_top + 10)

        # Company name in primary color
        c.setFillColor(primary_color)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin, footer_top - 10, "COMPANY NAME")

        # Contact information using secondary color for less emphasis
        c.setFillColor(secondary_color)
        c.setFont("Helvetica", 8)

        # Add contact details in columns
        # Column 1: Address
        address = "123 Business Avenue, Suite 500"
        city = "New York, NY 10001"
        c.drawString(margin, footer_top - 22, address)
        c.drawString(margin, footer_top - 32, city)

        # Column 2: Phone & Email (centered)
        phone = "Tel: (555) 123-4567"
        email = "info@companyname.com"

        # Calculate center position
        center_x = width / 2
        c.drawCentredString(center_x, footer_top - 22, phone)
        c.drawCentredString(center_x, footer_top - 32, email)

        # Column 3: Website & Social (right-aligned)
        website = "www.companyname.com"
        social = "LinkedIn: @companyname"

        # Right-aligned text
        website_width = c.stringWidth(website, "Helvetica", 8)
        social_width = c.stringWidth(social, "Helvetica", 8)

        c.drawString(width - margin - website_width, footer_top - 22, website)
        c.drawString(width - margin - social_width, footer_top - 32, social)

    # To use this in your existing code, add it just before c.save():
    # add_company_footer(c, width, height, primary_color, secondary_color)

    add_company_footer(c, width, height, primary_color, secondary_color)

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
