from pydantic import BaseModel 
from typing import Optional, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

class CourseData(BaseModel):
    Year1_Semester1: List[str]
    Year1_Semester2: List[str]
    Year1_SpecialSemester: Optional[List[str]]
    Year2_Semester1:List[str]
    Year2_Semester2: List[str]
    Year3_Semester1: List[str]
    Year3_Semester2: List[str]
    Year4_Semester1: List[str]
    Year4_Semester2: Optional[List[str]]
    Year5_Semester1: Optional[List[str]]
    Year5_Semester2: Optional[List[str]]
    Year3_SpecialSemester: Optional[List[str]]

model = AzureChatOpenAI(model="gpt-4o-mini-lke")
# model = AzureChatOpenAI(model="ANV2Exp-AzureOpenAI-NorthCtrlUS-TWY-GPT4o")

def generate_updated_roadmap(original_course_plan, completed_courses):
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

    print(generate_output)

    return generate_output
    

if __name__ == "__main__":
    generate_updated_roadmap({
        "Year1_Semester1": ["SC1003", "SC1005", "SC1013", "MH1810", "MH1812", "CC0003", "CC0005", "HW0001"],
        "Year1_Semester2": ["SC1004", "SC1006", "SC1007", "EG1001", "SC1015", "CC0001", "CC0002"],
        "Year1_SpecialSemester": None,
        "Year2_Semester1": ["SC2000", "SC2001", "SC2002", "SC2005", "CC0007", "BDE"],
        "Year2_Semester2": ["SC2006", "SC2008", "SC2207", "SC3000", "CC0006", "ML0004", "BDE"],
        "Year3_Semester1": ["SC3010", "SC3xxx", "SC3xxx", "SC2079", "HW0288", "BDE"],
        "Year3_Semester2": ["SC3079"],
        "Year4_Semester1": ["SC4079", "SC4xxx", "SC4xxx", "BDE", "BDE"],
        "Year4_Semester2": ["SC4079", "SC4xxx", "SC4xxx", "BDE", "BDE"],
        "Year5_Semester1": None,
        "Year5_Semester2": None,
        "Year3_SpecialSemester": None
    }, 
    [
        {'Year1_Semester1': [{'courseCode': 'CC0003', 'courseType': 'C'}, {'courseCode': 'CC0005', 'courseType': 'C'}, {'courseCode': 'MH1810', 'courseType': 'C'}, {'courseCode': 'MH1812', 'courseType': 'C'}, {'courseCode': 'SC1003', 'courseType': 'C'}, {'courseCode': 'SC1005', 'courseType': 'C'}, {'courseCode': 'SC1013', 'courseType': 'C'}], 'Year1_Semester2': [{'courseCode': 'CC0001', 'courseType': 'C'}, {'courseCode': 'CC0002', 'courseType': 'C'}, {'courseCode': 'EG1001', 'courseType': 'C'}, {'courseCode': 'SC1004', 'courseType': 'C'}, {'courseCode': 'SC1006', 'courseType': 'C'}, {'courseCode': 'SC1007', 'courseType': 'C'}, {'courseCode': 'SC1015', 'courseType': 'C'}], 'Year1_SpecialSemester': None, 'Year2_Semester1': None, 'Year2_Semester2': None, 'Year3_Semester1': None, 'Year3_Semester2': None, 'Year4_Semester1': None, 'Year4_Semester2': None, 'Year5_Semester1': None, 'Year5_Semester2': None, 'Year3_SpecialSemester': None},
        {'Year1_Semester1': None, 'Year1_Semester2': None, 'Year1_SpecialSemester': None, 'Year2_Semester1': [{'courseCode': 'SC2005', 'courseType': 'C'}, {'courseCode': 'SC2001', 'courseType': 'C'}, {'courseCode': 'SC2000', 'courseType': 'C'}, {'courseCode': 'CC0007', 'courseType': 'C'}, {'courseCode': 'AAA18E', 'courseType': 'BDE'}, {'courseCode': 'SC2002', 'courseType': 'C'}], 'Year2_Semester2': [{'courseCode': 'SC2207', 'courseType': 'C'}, {'courseCode': 'SC2008', 'courseType': 'C'}, {'courseCode': 'SC2006', 'courseType': 'C'}, {'courseCode': 'CC0006', 'courseType': 'C'}, {'courseCode': 'ML0004', 'courseType': 'C'}, {'courseCode': 'SC3000', 'courseType': 'P'}], 'Year3_Semester1': None, 'Year3_Semester2': None, 'Year4_Semester1': None, 'Year4_Semester2': None, 'Year5_Semester1': None, 'Year5_Semester2': None, 'Year3_SpecialSemester': None}
    ]
)