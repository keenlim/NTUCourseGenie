import os 
from dotenv import load_dotenv
from functions.utils.llm.llm import gpt_4o_mini_azure
from functions.models.graph_states import OverallState, OutputState
from knowledge_base_manager.core.qna_manager import QnAManager
from knowledge_base_manager.core.knowledge_base_manager import KnowledgeBaseManager
from knowledge_base_manager.types import Category


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

        # Define question categories
        question_categories = [
            Category(title="COURSE_SELECTION", description="Questions about choosing courses, prerequisites, course recommendations, or course details.", example_question="What courses should I take if I am interested in AI?"),
            Category(title="COURSE_DETAILS", description="Questions about course content, schedules, or instructors.", example_question="Who is teaching the AI course this semester?"),
            Category(title="PROGRAM_REQUIREMENTS", description="Questions about program structures, credit requirements, or graduation criteria.", example_question="How many credits do I need to graduate?"),
            Category(title="ADMIN", description="Questions about enrolment processes, add/drop deadlines, or registration issues.", example_question="When is the last day to drop a course?"),
            Category(title="CAREER_GUIDANCE", description="Questions about career prospects, internships, or industry relevance of courses.", example_question="Which courses are best for a career in data science?"),
            Category(title="ACADEMIC_SUPPORT", description="Questions about tutoring, office hours, or academic assistance.", example_question="Are there any tutoring sessions for this course?"),
            Category(title="GENERAL_INFO", description="General questions about NTU, CCDS, or campus facilities.", example_question="Where is the CCDS building located?"),
            Category(title="UNCATEGORISED", description="Questions that do not clearly fit into any of the above categories.", example_question="Which professor is in charge of SC2009?"),
            Category(title="IRRELEVANT", description="Questions that are unrelated to the course or inappropriate.", example_question="What’s the best coffee shop near campus?")
        ]

        # Initialise QnA Manager 
        self.qna_manager = QnAManager(db_connection_str=os.environ.get("MONGODB_HOST"),
                                      db_name="coursegenie",
                                      collection_name="qnaDocument",
                                      llm=self.llm,
                                      rephrase_question=True,
                                      categorise_question=True,
                                      categories=question_categories)

        # Initialise Knowledge base manager 
        self.kb_manager = KnowledgeBaseManager(
            azure_text_embedding_config={
                "azure_deployment": os.environ.get("TEXT_EMBEDDING_MODEL_DEPLOYMENT"),
                "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
                "endpoint": os.environ.get("AZURE_OPENAI_ENDPOINT"),
                "model": os.environ.get("TEXT_EMBEDDING_MODEL_NAME")
            },
            azure_ai_search_config={
                "endpoint": os.environ.get("AZURE_AI_SEARCH_ENDPOINT"),
                "api_key": os.environ.get("AZURE_AI_SEARCH_API_KEY")
            },
            index_name="coursegenie-qna"
        )

    def feedback(self, query: str, chat_history: list):
        
        # Retrieve context
        docs = self.kb_manager.similarity_search(query, top_k=3)
        context = "\n".join(doc["content"] for doc in docs)

        # FOR DEBUGGING
        print("Context retrieved: ", context)

        # Classify query: check if query can be answered with existing qna list 
        response = self.classify_query(context, query)

        if "QUERY" in response: # If codeword QUERY is found, means that question couldn't be answered
            # Add question to QnA list 
            self.qna_manager.resolve_non_trivial_query(chat_history)

            # Return the retrieved information or the standard default response
            return "Sorry, I am unable to answer your question. I have forwarded your question to your course instructor."
        else:
            # If the query can be answered, return the response
            return response
    
    def classify_query(self, context_str:str, query: str):
        # Form system prompt 
        system_prompt = f"""
                        You are given a context and a query. Determine whether the context provides sufficient information to answer the query.

                        If the context is enough to answer the query, respond to the query using the context.

                        If the context is insufficient to answer the query, respond with "QUERY" only.

                        Context: {context_str}
                        Query: {query}
                        """
        
        llm_response = self.llm.invoke(system_prompt).content 
        return llm_response
    
    def sync_qna_to_kb(self):
        # generate a new qna document and update kb
        return self.kb_manager.fetch_and_index_cosmosdb_data(qna_manager=self.qna_manager)

    def create_index(self):
        return self.kb_manager.create_index()
    

    def feedback_node(self, state: OverallState) -> OverallState:
        """
        Feedback node to retrieve relevant responses
        """
        query = state.get("query")[-1]
        chat_history = state.get("messages")

        # Add into Database records
        feedback_output = self.feedback(query, chat_history)

        return {
            "database_records": feedback_output,
            "next_action": "end",
            "steps": ["feedback_retrieval"]
        }


        