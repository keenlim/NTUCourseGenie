from functions.models.agent_types import History_Query
from langchain_core.prompts import PromptTemplate
from functions.utils.llm.llm import gpt_4o_mini_azure

# History Aware Retriever Agent - To rephrase the query based on previous chat messages
def history_retriever(query, context):
    system_template = """
                      You are provided with the following chat history as context below:
                      {context}

                      Given this context, please review the user's query below. You need to decide if the queries are related to each other. 

                      You will only need to rewrite the query if the query contains the following pronouns that suggests a certain entity that was provided before.: "it"
                      
                      If necessary, rewrite or rephrase the query to better align with the context, ensuring clarity and relevance. If the original query is already clear, you may leave it unchanged. 

                      Original Query: 
                      {query}
                      """
    
    prompt = PromptTemplate.from_template(system_template)
    structured_lm_formulation = gpt_4o_mini_azure().with_structured_output(History_Query)
    query_formulation = prompt | structured_lm_formulation

    results = query_formulation.invoke({"query": query, "context": context})

    return results.rewritten_query

def history_retriever_node(state):

    query = state["query"][0]
    chat_history = state["cached_messages"]
    print(chat_history)
    response = history_retriever(query, chat_history)

    return {"query": [response]}