from langchain_core.prompts import PromptTemplate 
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Neo4jVector
from functions.models.agent_types import UpdateQuery, SearchList
from functions.utils.neo4j.graph_examples import graph_few_shot_examples
from functions.utils.llm.llm import azure_text_embedding, gpt_4o_mini_azure


def rewrite_query(query: str, retrieverResults, entities: SearchList, user_profile: dict):
    examples = graph_few_shot_examples()

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples, 
        azure_text_embedding(), 
        Neo4jVector, 
        k=3,
        input_keys=["question"]
    )

    NL = "\n"
    fewshot_examples = (NL).join(
        [
            f"Question: {el['question']}{NL}"
            for el in example_selector.select_examples(
                {"question": query}
            )
        ]
    )

    print(fewshot_examples)

    # Format user_profile information into a String
    user_information = f"Degree: {user_profile['degree']} \n Year Standing: {user_profile['year_standing']} \n Most Recently Completed Semester: {user_profile['semester']}"

    system_template = """
                    You are a question re-writer that converts an input question to a better version that is optimised. Look at the input and try to reason about the underlying semantic intent or meaning. 

                    You are given the original query where you are tasked to rewrite the query by replacing the entities identified previously to specific unique identifiers. 

                    The retriever have return the top 5 similar results based on full-text search, based on the retrieved information, you will select the unique identifier to replace the entities. 

                    In addition, you will also be provided with user profiling information. Specific user information are as follows: degree, year_standing and the semester that users have completed. 
                    - If user ask for next semester, you have to determine what is their next semester. There are only 2 semesters in the year, Semester 1 and Semester 2. For example, if user is currently in Year 1 and Semester 2, the next semester would be Year 2 Semester 1. You should rewrite and improve the query accordingly. 

                    Examples of closest match questions are also provided. Hence, you should structure the query to match the examples. 
                    NOTE: If the original query does not contain any wording 'next semester', you SHOULD NOT need to provide information about the semesters. 

                    If the original query contains information about a specific year and semester, you should refer to the year and semester information provided from the query. Do NOT Change the year and semeseter information from the original query.

                    The user information should not overwrite the original query. You should also not exclue any 'type' information of courses such as 'ICC', 'MPE', 'BDE' from the query

                    Original Query: 
                    {query}

                    Retrieved Results: 
                    {retrievedResults}

                    Entities: 
                    {entities}

                    Examples:
                    {fewShot_examples}

                    User Profile Information: 
                    {user_information}
                      """
    prompt = PromptTemplate.from_template(system_template)

    entity = entities.model_dump()
    structured_llm_formulation = gpt_4o_mini_azure().with_structured_output(UpdateQuery)

    rewrite_query = prompt | structured_llm_formulation
    results = rewrite_query.invoke({"query": query, "retrievedResults": retrieverResults, "entities": entity, "fewShot_examples": fewshot_examples, "user_information": user_information})

    return results.updatedQuery


def rewrite_query_node(state):
    query = state["query"][-1]
    retrieverResults = state["entity"][-1]
    entities = state["entity"][-2]
    user_profile = state["user_profile"]

    # Response
    response = rewrite_query(query, retrieverResults, entities, user_profile)
    # print(response)
    return {"query": [response]}