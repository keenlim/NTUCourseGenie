# Extract Course Information from Images using GPT4o Accurately
from pydantic import BaseModel, Field
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Optional, Literal
from dotenv import load_dotenv

load_dotenv(override=True)

model = AzureChatOpenAI(model="ANV2Exp-AzureOpenAI-NorthCtrlUS-TWY-GPT4o", temperature=0)

class CourseImage(BaseModel):
    Code: str = Field(description="Specific Course Code of each course, for example 'SC1005'")
    Title: str = Field(description="Specific Course Title of each course, for example 'Digital Logic'")
    Grades: str = Field(description="Grades extracted from each course, for example 'A'")
    is_Completed: bool = Field(description="By default will be True")

class Courses(BaseModel):
    Course: List[CourseImage]

class CourseInfo(BaseModel):
    courseCode: str = Field(description="Specific course code")
    courseType: Literal['C', 'P', 'BDE'] = Field(description="Course Type, C suggests Core, P suggests MPE, BDE suggests BDE courses")

class CourseData(BaseModel):
    Year1_Semester1: Optional[List[CourseInfo]]
    Year1_Semester2: Optional[List[CourseInfo]]
    Year1_SpecialSemester: Optional[List[CourseInfo]]
    Year2_Semester1: Optional[List[CourseInfo]]
    Year2_Semester2: Optional[List[CourseInfo]]
    Year3_Semester1: Optional[List[CourseInfo]]
    Year3_Semester2: Optional[List[CourseInfo]]
    Year4_Semester1: Optional[List[CourseInfo]]
    Year4_Semester2: Optional[List[CourseInfo]]
    Year5_Semester1: Optional[List[CourseInfo]]
    Year5_Semester2: Optional[List[CourseInfo]]
    Year3_SpecialSemester: Optional[List[CourseInfo]]


def analyse_image(base64Image):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Extract the relevant course information from the Image below."),
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

    response = image_chain.invoke({"image_data": base64Image})

    # print(response)
    return response

def analyse_course_image(base64Image):
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
    print(course_response)

    return course_response




