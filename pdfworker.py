import os
import fitz  # PyMuPDF for PDF extraction
import openai
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables for security
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


class PDFProcessor:
    def __init__(self, pdf_path):
        """
        Initialize the PDF processor with the path to the developer's PDF.

        Args:
            pdf_path (str): Path to the PDF file to process
        """
        self.pdf_path = pdf_path
        self.text_content = self._extract_text_from_pdf()

    def _extract_text_from_pdf(self):
        """Extract text content from the PDF file."""
        try:
            doc = fitz.open(self.pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return ""

    # Replace the _call_openai_api method with this:
    def _call_openai_api(self, prompt):
        """Make a call to OpenAI API with the given prompt using the new API."""
        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)

            response = client.chat.completions.create(
                model="gpt-4-turbo",  # Use the appropriate model
                messages=[
                    {"role": "system",
                     "content": "You are a helpful assistant that extracts real estate information from documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Low temperature for more factual responses
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return None

    def extract_property_description(self):
        """
        Extract a compelling property description from the PDF.

        Returns:
            list: A list of strings, each representing a line of the description
        """
        prompt = f"""
        Based on the following content extracted from a property development PDF, 
        create a compelling 5-line property description highlighting the key selling points.
        Format the response as a simple list of 5 text lines, each line should be 80-100 characters.

        PDF CONTENT:
        {self.text_content[:8000]}  # Limiting content to avoid token limits
        """

        response = self._call_openai_api(prompt)
        if response:
            # Process the response to get a list of lines
            lines = [line.strip() for line in response.strip().split('\n') if line.strip()]
            return lines[:5]  # Ensure we return at most 5 lines
        else:
            return [
                "This premium investment property offers an exceptional opportunity in an excellent location.",
                "Features include modern amenities and high-quality finishes throughout the development.",
                "Ideal for investors looking for strong returns in a growing market with high demand.",
                "The property offers versatile options suitable for various residential requirements.",
                "Secure this opportunity to acquire a property with significant appreciation potential."
            ]

    def extract_available_units(self):
        """
        Extract available units with details from the PDF.

        Returns:
            list: A list of dictionaries, each containing unit details
        """
        prompt = f"""
        Based on the following content extracted from a property development PDF, 
        identify and list the available units with their details.

        For each unit, extract:
        - Unit Number/ID
        - Size (in sq ft)
        - Price
        - Number of bedrooms/bathrooms (if available)
        - Any special features

        Format your response as a valid JSON array of objects, with each object representing a unit.

        PDF CONTENT:
        {self.text_content[:8000]}  # Limiting content to avoid token limits
        """

        response = self._call_openai_api(prompt)

        try:
            # Try to parse the response as JSON
            units = json.loads(response)
            return units
        except:
            # If JSON parsing fails, return default placeholder data
            print("Failed to parse available units data. Using placeholder data.")
            return [
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


def process_developer_pdf(pdf_path):
    """
    Process a developer's PDF and extract property information.

    Args:
        pdf_path (str): Path to the developer's PDF

    Returns:
        tuple: (description_lines, available_units)
    """
    processor = PDFProcessor(pdf_path)

    # Extract property description
    description_lines = processor.extract_property_description()

    # Extract available units
    available_units = processor.extract_available_units()

    return description_lines, available_units


if __name__ == "__main__":
    # Example usage
    pdf_path = "developer_brochure.pdf"

    if os.path.exists(pdf_path):
        description, units = process_developer_pdf(pdf_path)

        print("PROPERTY DESCRIPTION:")
        for line in description:
            print(line)

        print("\nAVAILABLE UNITS:")
        for unit in units:
            print(f"Unit: {unit.get('unit_id')}, Size: {unit.get('size')} sq ft, Price: {unit.get('price')}")
    else:
        print(f"File not found: {pdf_path}")
