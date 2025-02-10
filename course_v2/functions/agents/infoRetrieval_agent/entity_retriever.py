from functions.models.agent_types import SearchList
from functions.utils.AISearch.aisearch_retriever import AISearch_retriever

# Entity Retriever Agent
def entity_retriever(entities_query: SearchList):
    results = {}
    searchlists = entities_query.searchList 
    for searchlist in searchlists:
        queries = searchlist.queries 
        program = searchlist.program 
        for query in queries:
            if program == 'COURSE':
                course_results = AISearch_retriever(query).course_retriever()
                results[query] = course_results 
            elif program == 'DEGREE':
                degree_results = AISearch_retriever(query).degree_retriever()
                results[query] = degree_results 
        
    return results 


# Entity Retriever Nodes
def entity_retriever_node(state):
    entities_query = state["entity"][-1]
    response = entity_retriever(entities_query)
    return {"entity": [response]}

