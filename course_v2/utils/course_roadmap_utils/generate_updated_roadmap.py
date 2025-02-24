from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from ..Logger import setup_logger
from ..models.roadmap import CourseData

model = AzureChatOpenAI(model="gpt-4o-mini-lke", temperature=0)
# model = AzureChatOpenAI(model="o1-mini-lke")

def generate_updated_roadmap(original_course_plan, completed_courses):
    """
    Generate updated course roadmap based on the original default course plan and Completed course provided by students

    Attributes:
        original_course_plan (List[dict]): List of courses based on the default course plan
        completed_courses: (CourseData): Courses data structured in CourseData 
    
    Raises:
        ValueError: If there is a problem converting the data
        ConnectionError: If there is network or connection-related errors
        Exception: If there are any other errors
    """

    logging = setup_logger()
    logging.info("----------- Generate Course Roadmap ----------")

    try:
        system_template = """
                        You are an academic program planer. Your task is to analyse a student's academic progress and propose an updated study plan. The user will provide:
                        1. An original study roadmap for a 4-year (or 5-year) degree plan, broken down by semesters (e.g. Year3_Semester1, Year4_Semester2, etc)
                        2. A list of completed modules, orgainsed by semesters, showing modules already taken. 
                        
                        Your job is to:
                        1. Compare the original course roadmap with the completed moduels to identify:
                        - Modules that have already been completed.
                        - Modules that are still missing from the original roadmap.
                        2. Redistribute any missing modules into upcoming semester logically:
                        - Place any missing modules from earlier yers (e.g. Year 1 or Year 2) into upcoming semesters (e.g. Year 3 or Year 4)
                        - Avoid duplicating modules that have already been completed.
                        - Ensure semseter workloads are balanced while respecting the structure of the original roadmap.
                        - You should also ensure the students complete the correct number of MPE. 
                        3. Retain placeholders for electives (SC3xxx, SC4xxx, or BDE) from the original roadmap and include these in the updated plan where appropriate.
                        - For completed BDE, you should replace it with the completed module course code.
                        - For completed MPE, you should replace it with the completed module course code.
                        - You should keep track of the number of MPE that the student still need to complete.
                        4. Output the final course plan in JSON format, structured as follows:
                        {{
                            "Year1_Semester1": ["Completed_Module1", "Completed_Module2", ...],
                            "Year1_Semester2": ["Completed_Module1", ...],
                            "Year1_SpecialSemester": null,
                            "Year2_Semester1": ["Remaining_Module1", "Completed_Module1", ...],
                            ...
                            "Year4_Semester2": ["Remaining_Module1", ...],
                            "Year5_Semester1": null,
                            "Year5_Semester2": null,
                            "Year3_SpecialSemester": null
                        }}
                        5. MOOC course codes are considered BDE. These are courses students takes using online learning platform that can be considered as BDE. It should not be confused with MPE courses. 

                        If the semester has no modules left to be taken, then it should be null. 
                        """
        
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_template),
                ("human", "Original Course Plan: {original_course_plan}"),
                ("human", "Completed Course: {completed_course}"),
            ], 
        )

        generate_chain = prompt | model.with_structured_output(CourseData)

        generate_output = generate_chain.invoke({"original_course_plan": original_course_plan, "completed_course": completed_courses})

        # print(generate_output)

        return {
            "status": "success",
            "result": generate_output
        }
    except ValueError as e:
        logging.exception("ValueError while generating updated course roadmap")
        return {
            "status": "error",
            "message": "Invalid or corrupted data"
        }
    except ConnectionError as e:
        logging.exception("ConnectionError while generating updated course roadmap")
        return {
            "status": "error",
            "message": "Connection Error"
        }
    except Exception as e:
        logging.exception("Unexpected Error while generating updated course roadmap")
        return {
            "status": "error",
            "message": "Unexpected Error while generating updated course roadmap"
        }

    