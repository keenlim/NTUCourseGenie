import os
import base64
from io import BytesIO
from .convert_pdf_to_image import convert_pdf_to_image
from .analyse_image import analyse_image
from ..Logger import setup_logger

def process_files(uploaded_files):
    """
    Process the uploaded files and return the extracted data

    Attributes:
        uploaded_files (dict): Dictionary of uploaded files

    Returns:
        courseData (list): List of extracted data from the uploaded files
        imageData (list): List of extracted images in base64 encoding
        status (str): Status of the process
        message (str): Message for the process status
    """
    logging = setup_logger()
    logging.info("----------- Processing files ----------")
    all_course = []
    image_uploaded = []
    for uploaded_file in uploaded_files:
        # 1. Check the uploaded file type via the file extension
        filename = uploaded_file.name
        file_extension = os.path.splitext(filename)[1]
        # 2. If is PDF --> Convert to Image
        if file_extension == ".pdf":
            # Convert to Image
            bytes_data = uploaded_file.getvalue()
            images = convert_pdf_to_image(bytes_data)
            if images['status'] == "error":
                print("Error")
                return {"courseData": [], "imageData": [], "status": "error", "message": "Error analysing PDF"}

            for img in images['image']:
                try:
                    # 3. Once converted to image, convert to base64 and analyse the image
                    im_file = BytesIO()
                    img.save(im_file, format="JPEG")
                    im_bytes = im_file.getvalue()
                    encoded = base64.b64encode(im_bytes).decode("utf-8")
                    image_uploaded.append(encoded)
                    response = analyse_image(encoded)
                    response_status = response.get('status', None)
                    if response_status == "error":
                        return {"courseData": [], "imageData": [], "status": "error", "message": "Unexpected Error"}
                    course_response = response.get('result', None).dict(by_alias=True)
                    all_course.extend(course_response['Course'])
                except Exception as e:
                    print(f"Error: {e}")
                    return {"courseData": [], "imageData": [], "status": "error", "message": "Unable to analyse transcript"}

        else:
            try:
                # Upload image then just convert to base64 and analyase the image
                bytes_data = uploaded_file.getvalue()
                encoded = base64.b64encode(bytes_data).decode("utf-8")
                image_uploaded.append(encoded)
                response = analyse_image(encoded)
                response_status = response.get('status', None)
                if response_status == "error":
                    return {"courseData": [], "imageData": [], "status": "error", "message": "Unexpected Error"}
                course_response = response.get('result', None).dict(by_alias=True)
                all_course.extend(course_response['Course'])
            except Exception as e:
                print(f"Error: {e}")
                return {"courseData": [], "imageData": [], "status": "error", "message": "Unable to analyse transcript"}
    
    logging.info("---- Successfully analysed image ----")
    return {
        "courseData": all_course,
        "imageData": image_uploaded,
        "status": "success",
        "message": "Successfully analysed the uploaded files"
    }