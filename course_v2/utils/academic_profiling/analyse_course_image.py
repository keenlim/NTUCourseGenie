import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ..models.course import CourseData
from dotenv import load_dotenv 
from ..Logger import setup_logger


load_dotenv(override=True)
model = AzureChatOpenAI(model=os.getenv('AZURE_OPENAI_DEPLOYMENT_4o_NAME'), temperature=0)
def analyse_course_image(base64Image):
    """
    Extract relevant course information from Image provided and preprocess the data.

    Attributes:
        base64Image (str): Base64 encoded image data
    
    Returns:
        status (str): Status of the process
        result (CourseData): Course data extracted from the image
    
    Raises:
        Exception: If there is any errors
    """
    try:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("""system", "Extract the relevant course information from the Image below. 
                Extract the Course Code such as CC0003, SC4000 and place it in the relevant year and semester. 
                For example: {{"Year1_Semester1": ["SC1003", "SC1013", "MH1810", "EG1001", "AB1202", "AB1301", "CC0003", "CC0005"]}}"""),
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

        course_chain = prompt | model.with_structured_output(CourseData)
        course_response = course_chain.invoke({"image_data": base64Image})
        # print(course_response)

        return {"status": "success", "result": course_response}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": "Error while processing data"}