from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Literal
from langchain_openai import AzureChatOpenAI
"""
Provide Career Recommendation using Large Language Model based on the following parameters:
- Degree (Computer Engineering, Computer Science, DSAI, BCG, BCE, CSEcons, CEEcons)
- Career Interest (Their interest)
- Mods and Grades of the Mods taken

Output:
- Career Recommendation (:Literal)
- Explanation (:str)
- Strength (:str)
- Weakness (:str)
"""

model = AzureChatOpenAI(model="gpt-4o-mini-lke")

class CareerFeedback(BaseModel):
    career: Literal["Blockchain Engineer", "DevOps Engineer", "Cloud Engineer/Architect", "Mixed/Virtual Reality Developer", "Cyber Security", "Software Engineer", "Full-stack Developer", "Front-End Engineer / Web Developer", "Backend Engineer", "Data Engineer", "Business Analyst", "Firmware Engineer", "Computer Hardware Engineer", "Embedded System Developer","AI Engineer", "Machine Learning Engineer", "Data Scientist", "Data Analyst", "AI Scientist", "System Architect", "Cybersecurity Consultant/Analyst", "Product Manager", "Entrepreneur", "Quantitative Analyst/Developer"] = Field(
        description="Career recommendation based on the courses and grades."
    )
    explanation: str = Field(description="Provide a detailed explanation of why you recommend the career")
    strength: str = Field(description = "Short description of the strength of the student")
    weakness: str = Field(description="Short description of the weakness of the student")

def career_feedback(degree, career_interest, courses_taken):
    system_template = """
                      You are to act as a career advisor who aims to help students to provide a personalise course plan suited to their strengths and career interests. 

                      You will be provided with the degree the student is currently studying, their career interests as well as a list of courses they have completed together with the respective grades. 

                      Based on these information, you are to meticulously evaluate their strength and weakness and recommend a specific career they should consider. You are to provide a detailed explanation on why is the student fitted for the role as well as short evaluation of their strength and weaknesses. 

                      Grading System:
                      Letter Grade: A+, A, A-, B+, B, B-, C+, C, D+, D, F
                      F: Fail
                      P: Pass (For pass/fail courses)
                      EX: Exempted from course
                      S: Satisfactory
                      U: Unsatisfactory

                      A pass/fail course are usually fundamental courses by the school to allow students to bridge the gap. 

                      Degree: 
                      {degree}

                      Career Interest:
                      {career_interest}

                      Course Completed:
                      {courses_taken}
                      """
    career_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_template,
            )
        ]
    )

    career_chain = career_prompt | model.with_structured_output(CareerFeedback)
    career_output = career_chain.invoke({"degree": degree, "career_interest": career_interest, "courses_taken": courses_taken})
    # print(career_output)

    return career_output
    


if __name__ == "__main__":
    # career_feedback("Computer Science", ["AI Engineer", "Full-Stack Developer"], [{'Code': 'CC0001', 'Title': 'INQUIRY & COMMUNICATION IN AN INTERDISCIPLINARY WORLD', 'Grades': 'B+', 'is_Completed': True}, {'Code': 'CC0002', 'Title': 'NAVIGATING THE DIGITAL WORLD', 'Grades': 'A-', 'is_Completed': True}, {'Code': 'EG1001', 'Title': 'ENGINEERS IN SOCIETY', 'Grades': 'B+', 'is_Completed': True}, {'Code': 'SC1004', 'Title': 'LINEAR ALGEBRA FOR COMPUTING', 'Grades': 'A+', 'is_Completed': True}, {'Code': 'SC1006', 'Title': 'COMPUTER ORGANISATION & ARCHITECTURE', 'Grades': 'A-', 'is_Completed': True}, {'Code': 'SC1007', 'Title': 'DATA STRUCTURES & ALGORITHMS', 'Grades': 'A-', 'is_Completed': True}, {'Code': 'SC1015', 'Title': 'INTRODUCTION TO DATA SCIENCE & ARTIFICIAL INTELLIGENCE', 'Grades': 'A+', 'is_Completed': True}, {'Code': 'CC0003', 'Title': 'ETHICS & CIVICS IN A MULTICULTURAL WORLD', 'Grades': 'A-', 'is_Completed': True}, {'Code': 'CC0005', 'Title': 'HEALTHY LIVING & WELLBEING', 'Grades': 'A-', 'is_Completed': True}, {'Code': 'MH1810', 'Title': 'MATHEMATICS 1', 'Grades': 'EX', 'is_Completed': True}, {'Code': 'MH1812', 'Title': 'DISCRETE MATHEMATICS', 'Grades': 'B+', 'is_Completed': True}, {'Code': 'SC1003', 'Title': 'INTRODUCTION TO COMPUTATIONAL THINKING & PROGRAMMING', 'Grades': 'A-', 'is_Completed': True}, {'Code': 'SC1005', 'Title': 'DIGITAL LOGIC', 'Grades': 'A', 'is_Completed': True}, {'Code': 'SC1013', 'Title': 'PHYSICS FOR COMPUTING', 'Grades': 'P', 'is_Completed': True}])
    career_feedback("Computer Science", ["AI Engineer"], None)