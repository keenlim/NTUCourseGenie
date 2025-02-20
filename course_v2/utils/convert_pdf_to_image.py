from pdf2image import convert_from_bytes
from pdf2image.exceptions import (
    PDFPopplerTimeoutError,
    PDFPageCountError,
    PDFSyntaxError,
    PDFInfoNotInstalledError
)

# Convert pdf_to_iamge using pdf2image python library
def convert_pdf_to_image(pdf_file):
    try:
        images = convert_from_bytes(pdf_file)
        # for i, img in enumerate(images):
        #     img.save(f"/Users/keenlim/Final-Year-Project/Development/Course_v2/course_v2/utils/images/output_{i}.jpg", 'JPEG')
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