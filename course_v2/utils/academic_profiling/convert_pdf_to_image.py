from pdf2image import convert_from_bytes
from pdf2image.exceptions import (
    PDFPopplerTimeoutError,
    PDFPageCountError,
    PDFSyntaxError,
    PDFInfoNotInstalledError
)

# Convert pdf_to_iamge using pdf2image python library
def convert_pdf_to_image(pdf_file):
    """
    Convert a PDF file to an image using pdf2image library

    Attributes:
        pdf_file (bytes): PDF file content as bytes
    
    Returns:
        images (list[PIL]): List of images extracted from the PDF file
        status (str): Status of the conversion process
    
    Raises:
        NotImplementedError: If pdf2image is not supported on the system
        PDFPopplerTimeoutError: If pdf2image failed to convert the PDF file
        PDFPageCountError: If pdf2image failed to convert the PDF file
        PDFSyntaxError: If pdf2image failed to convert the PDF file
        PDFInfoNotInstalledError: If pdf2image failed to convert the PDF file
        Exception: If there is any other errors
    """
    try:
        images = convert_from_bytes(pdf_file)
        return {"image": images, "status": "success"}
    except NotImplementedError:
        print("NotImplementedError: pdf2image is not supported on this system")
        return {"status": "error"}
    except PDFPopplerTimeoutError:
        print("PDFPopplerTimeoutError: pdf2image failed to convert the PDF file")
        return {"status": "error"}
    except PDFPageCountError:
        print("PDFPageCountError: pdf2image failed to convert the PDF file")
        return {"status": "error"}
    except PDFSyntaxError:
        print("PDFSyntaxError: pdf2image failed to convert the PDF file")
        return {"status": "error"}
    except PDFInfoNotInstalledError:
        print("PDFInfoNotInstalledError: pdf2image failed to convert the PDF file")
        return {"status": "error"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error"}