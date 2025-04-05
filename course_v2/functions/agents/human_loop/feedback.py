import os 
from dotenv import load_dotenv
from functions.utils.llm.llm import gpt_4o_mini_azure
from functions.models.graph_states import OverallState, OutputState


load_dotenv(override=True)

class FeedbackRetrieval:
    """
    This class is used to handle feedback from the 
    human-in-a-loop pipeline
    """
    def __init__(self):
        # Initialise all the variables needed 

        # Initialise the LLM used in QnAManager
        self.llm = gpt_4o_mini_azure()

        # Initialise QnA Manager 

        # Initialise Knowledge base manager 

    def feedback(self, query: str):
        # TODO: Put the entire feedback pipeline here

        # Return the retrieved information or the standard default response
        return "Sorry, I am unable to answer your question. I have forwarded your question to your course instructor."
    

    def feedback_node(self, state: OverallState) -> OverallState:
        """
        Feedback node to retrieve relevant responses
        """
        query = state.get("query")[-1]

        # Add into Database records
        feedback_output = self.feedback(query)

        return {
            "database_records": feedback_output,
            "next_action": "end",
            "steps": ["feedback_retrieval"]
        }


        

