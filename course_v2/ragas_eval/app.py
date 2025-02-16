from ragas import SingleTurnSample
from ragas.metrics import BleuScore
from functions.workflow.retrieval_workflow import Retrieval_Workflow

class Ragas_app:
    def __init__(self):
        pass

    def evaluate(self):
        # Testing with empty history messages, and empty user profile 
        cached_messages = []
        user_profile = {}

        # Load dataset from CSV file
        

        # Initialise the workflow
        workflow = Retrieval_Workflow().workflow_function()



if __name__ == "__main__":
    evaluation = Ragas_app().evaluate()