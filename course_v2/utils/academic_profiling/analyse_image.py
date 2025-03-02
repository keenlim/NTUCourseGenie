# Extract Course Information from Images using GPT4o Accurately
import os
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ..models.course import Courses
from dotenv import load_dotenv 
from ..Logger import setup_logger

load_dotenv(override=True)
model = AzureChatOpenAI(model=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'), temperature=0)
# model = ChatOpenAI(model="gpt-4o", temperature=0)

def analyse_image(base64Image:str):
    """
    Extract relevant course and grades information from the Image provided

    Attributes:
        base64Image (str): Base64 encoded image data
    
    Returns: 
        course_data (Courses): Course data extracted from the image 
        status (str): Status of the extraction process
    
    Raises:
        ValueError: If there is problem decoding base64 or converting data 
        ConnectionError: If there is network or connection-related errors 
        Exception: If there is any other errors
        
    """
    logging = setup_logger()
    logging.info("----------- Analyse Image ----------")

    try:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", 
                 """
                 Extract the relevant course information from the Image below. 
                 You are to extract the following information: 
                 - Specific Code of the Course 
                 - Specific Title of the Course 
                 - Grade of each course
                 - Whether the course is completed or not, by default it is True 
                 - Course Type, Core (C), MPE (P), BDE (BDE)
                 - Year and Semester of the course, e.g. Year1_Semester1
                 """
                ),
                (
                    "user",
                    [
                        {
                            "type": "image_url",
                            "image_url": {"url": "data:image/jpeg;base64,{image_data}"},
                        }
                    ],
                ),
            ]
        )

        structured_llm = model.with_structured_output(Courses)

        image_chain = prompt | structured_llm

        response = {"result": image_chain.invoke({"image_data": base64Image}), "status": "success"}
        logging.info("---- Successfully analysed image ----")
        return response
    except ValueError as e:
        logging.exception("ValueError while analysing image")
        return {
            "status": "error",
            "message": "Invalid or corrupted image"
        }
    except ConnectionError as e:
        logging.exception("ConnectionError while analysing image")
        return {
            "status": "error",
            "message": "Connection Error"
        }
    except Exception as e:
        logging.exception("Unexpected Error while analysing image")
        return {
            "status": "error",
            "message": "Error while analysing image"
        }

