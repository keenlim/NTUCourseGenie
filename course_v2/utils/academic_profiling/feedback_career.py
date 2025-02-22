from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from ..Logger import setup_logger
from ..models.course import CareerFeedback
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

model = AzureChatOpenAI(model="gpt-4o-mini-lke",temperature=0)

def career_feedback(degree, career_interest, courses_taken):
    """
    Provide career recommendation based on User's degree, career interet and course taken

    Attributes:
        degree (str): Degree taken by student
        career_interest (str): Career interest of student
        courses_taken (list): List of courses taken by student

    Returns:
        CareerFeedback (CareerFeedback): Specific career feedback suggested 
        
    """
    logging = setup_logger()
    logging.info("----------- Career Feedback Function ----------")
    try:
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
    except Exception as e:
        logging.error(f"Error in career_feedback: {e}")
        return None