from langgraph.graph import END, StateGraph, START
from ..agents.infoRetrieval_agent.entity_identifier import entity_identifier_node
from ..agents.infoRetrieval_agent.entity_retriever import entity_retriever_node
from ..agents.infoRetrieval_agent.rewrite_query import rewrite_query_node
from ..models.graph_states import OverallState
from ..agents.infoRetrieval_agent.graph_retriever import GraphRetrieval
from .conditional_edges import validate_cypher_condition, guardrails_condition
from ..models.graph_states import InputState, OutputState
from ..agents.general_agent.guardrail_agent import guardrails_node
from ..agents.general_agent.history_agent import history_retriever_node
from langgraph.checkpoint.memory import MemorySaver

class Retrieval_Workflow():

    def __init__(self):
        pass

    def workflow_function(self):
        # Define Graph
        workflow = StateGraph(OverallState, input=InputState, output=OutputState)
        graph = GraphRetrieval()
        
        # Define Nodes (Agents)
        workflow.add_node("history", history_retriever_node)
        workflow.add_node("guardrails", guardrails_node)
        workflow.add_node("entity_identifier", entity_identifier_node)
        workflow.add_node("ai_search_retriever",entity_retriever_node)
        workflow.add_node("rewrite_query", rewrite_query_node)
        workflow.add_node("generate_cypher", graph.generate_cypher_node)
        workflow.add_node("validate_cypher", graph.validate_cypher_node)
        workflow.add_node("correct_cypher", graph.correct_cypher_node)
        workflow.add_node("execute_cypher", graph.execute_cypher_node)
        workflow.add_node("generate_final_answer", graph.generate_final_answer_node)


        # Define Edges
        workflow.add_edge(START, "history")
        workflow.add_edge("history", "guardrails")
        workflow.add_conditional_edges(
            "guardrails",
            guardrails_condition
        )
        workflow.add_edge("entity_identifier", "ai_search_retriever")
        workflow.add_edge("ai_search_retriever", "rewrite_query")
        workflow.add_edge("rewrite_query", "generate_cypher")
        workflow.add_edge("generate_cypher", "validate_cypher")
        workflow.add_conditional_edges(
            "validate_cypher",
            validate_cypher_condition
        )
        workflow.add_edge("execute_cypher", "generate_final_answer")
        workflow.add_edge("correct_cypher", "validate_cypher")
        workflow.add_edge("generate_final_answer", END)

        # Add Memory
        # memory = MemorySaver()
        graph = workflow.compile()
        png_data = graph.get_graph(xray=True).draw_mermaid_png()
        # Save the image data to a PNG file
        with open('graph.png', 'wb') as f:
            f.write(png_data)

        return graph

