import pdfplumber
import io

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts raw text content from a PDF file using pdfplumber.
    
    Args:
        pdf_file: A file path (str), file-like object, or bytes of the PDF.
        
    Returns:
        str: The extracted raw text.
    """
    text = ""
    try:
        # Check if the input is bytes, if so wrap in BytesIO
        if isinstance(pdf_file, bytes):
            pdf_file = io.BytesIO(pdf_file)
            
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error during PDF text extraction: {e}")
        
    return text.strip()
