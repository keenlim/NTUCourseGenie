# Entity_Identifier Agent
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.runnables import RunnablePassthrough
from functions.utils.llm.llm import gpt_4o_mini_azure
from functions.models.agent_types import SearchList

# Agent 
def entity_identifier(query: str):
    azure_llm = gpt_4o_mini_azure()
    system = """
             Based on the query given, you have the ability to issue search queries with the aim of rewriting the query by replacing these entities to specific unique identifies that can be retrieved from the database. 
             
             You should identify entities that is needed to be replaced with the unique identifiers such as courseCode (e.g. SC1003, SC1004, AB1001, MH1812) or degreeCode (e.g. 'CSC', 'CE', 'DSAI', 'BCG', 'BCE', 'CSEcons', 'CEEcons', 'MACS').

             When looking out for unique identifiers, you should only identify courseCode and degreeCode. DO NOT include any other information. 

             For example: 
             Query: Tell me more about SC1003. --> queries=['SC1003'], program='COURSE'
             Query: Tell me more about Digital Logic course --> queries=['Digital Logic'], program='COURSE'
             Query: What are the courses I need to take in Year 1 Semester 1 as a CSC Student? --> queries=['CSC'], program='DEGREE'

             You are able to route to two different database, where the `COURSE` database contains all the Course information, `DEGREE` database contains all Degree information. 

             Different entities can also belong to different database, hence you are to abstract all the entities and match to the correct database. 
             """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human",  "{question}")
        ]
    )

    structured_llm_formulation = azure_llm.with_structured_output(SearchList)
    query_formulation = {"question": RunnablePassthrough()} | prompt | structured_llm_formulation

    results = query_formulation.invoke(query)

    return results

# Nodes 
def entity_identifier_node(state):
    query = state["query"][-1]
    response = entity_identifier(query)

    return {"entity": [response]}
