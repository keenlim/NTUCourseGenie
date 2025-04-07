from langchain_core.prompts import ChatPromptTemplate
from functions.utils.llm.llm import gpt_4o_mini_azure
from functions.models.agent_types import GuardrailsOutput
from functions.models.graph_states import InputState, OverallState
from langchain_core.messages import HumanMessage

# Guardrails Agent - To sieve out questions that are unrelated to course planning
def guardrails(query: str):
    guardrails_system = """
                        You are a course advisor in Nanyang Technological University and you are only build with robust knowledge on Courses and Degrees offered in College of Computing and Data Science. You should decide whether the query is related to the courses, degrees, or information about schools. 

                        You are to: 
                        1. Analyse the User's Query: 
                            - Understand the semantic of user's query to check what is the main aim of the user's query. 
                        2. Decide on Query Type:
                            - If the query is related to Course Planning such as but not limited to course details, personalised course recomendations or any course specific information (e.g. Instructor of course, Course details, Examination schedules, Tutorial schedules), then you will respond with "courses". If the query is related to information about degree such as Computer Science programme, or query is related to school such as CCDS, you should also respond with "courses". 
                            - Only if the query asked by the user is unrelated to Course or Degree information, then respond with output "end"

                        Common terminology related to Course Planning:
                        - AU: Academic Units
                        - 3k: Level 3 modules
                        - 4k: Level 4 modules
                        - Mods: Modules / Courses
                        - MPE: Major Prescribed Elective
                        - BDE: Broadening and Deepening Elective
                        - Grad: Graduation

                        You have the ability in understanding complex semantic meaning of the query and providing the correct decision to the query type. 
                        """
    
    guardrails_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                guardrails_system
            ),
            (
                "human",
                ("{question}")
            ),
        ]
    )

    guardrails_chain = guardrails_prompt | gpt_4o_mini_azure().with_structured_output(GuardrailsOutput)
    guardrails_output = guardrails_chain.invoke({"question": query})

    return guardrails_output

def guardrails_node(state: InputState) -> OverallState:
    """
    Decides if the question is related to courses or not 
    """
    query= state.get("query")[-1]
    guardrails_output = guardrails(query)
    database_records = None 
    if guardrails_output.decision == "end":
        database_records = "Hello! 👋 I'm your friendly course assistant bot! This question is not related to course planning. Therefore, I am cannot answer this question. However, I'm here to help you with any questions about courses, including prerequisites and course codes. Just let me know what you need!"

    return {
        "messages": [HumanMessage(query)],
        "next_action": guardrails_output.decision, 
        "database_records": database_records, 
        "steps": ["guardrail"],
    }