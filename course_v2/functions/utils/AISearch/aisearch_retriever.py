import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from functions.utils.llm.llm import azure_text_embedding
from azure.search.documents.models import VectorizedQuery


load_dotenv(override=True)

class AISearch_retriever:
    # https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/basic-vector-workflow/azure-search-vector-python-sample.ipynb
    # Further Improvement : https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/advanced-workflow/query-rewrite/query-rewrite.ipynb
    def __init__(self, query):
        self.query = query # Query provided 
        self.endpoint = os.environ.get('AZURE_AI_SEARCH_ENDPOINT')
        self.credential = AzureKeyCredential(os.environ.get('AZURE_AI_SEARCH_API_KEY'))
        self.course_index_name = 'course-index-updated'
        self.degree_index_name = 'degree-index'
        self.embeddings = azure_text_embedding()

    # Retrieve context from course-index
    def course_retriever(self):
        # 1. Define search client 
        search_client = SearchClient(
            endpoint = self.endpoint,
            index_name = self.course_index_name,
            credential = self.credential
        )

        # 2. Embed the query --> To perform Vector Search
        embedding = self.embeddings.embed_query(self.query)
        vector_query = VectorizedQuery(vector=embedding, k_nearest_neighbors=3, fields="titleVector, descriptionVector,courseCodeVector")

        # 3. Retrieve the selected fields from the search index and vector index related to the question
        search_results = search_client.search(
            search_text=self.query, 
            vector_queries = [vector_query],
            top=5,
            select = ["courseCode", "academicUnits", "title", "description", "pre_requisite", "co_requisite"]
        )

        # 4. Initialise an empty list to hold formatted course information
        formatted_results = []

        for document in search_results:
            # Extract fields from the document, providing default values if necessary
            course_info = {
                "score": document.get("@search.score", ""),
                "courseCode": document.get("courseCode", ""),
                "title": document.get("title", ""),
                "description": document.get("description", ""),
                "academic_units": document.get("academicUnits", "")
            }

            # Add pre_requisite if it exist and is not empty
            pre_requisite = document.get("pre_requisite", "")
            if pre_requisite:
                course_info["pre_requisite"] = pre_requisite
            
            # Add co_requisite if it exist and is not empty
            co_requisite = document.get("co_requisite", "")
            if co_requisite:
                course_info["co_requisite"] = co_requisite
            
            formatted_results.append(course_info)

        # Return it in JSON format
        return formatted_results    
    
    def degree_retriever(self):
        # 1. Define search client
        search_client = SearchClient(
            endpoint = self.endpoint, 
            index_name = self.degree_index_name, 
            credential = self.credential
        )

        # 2. Embed the query --> To perform Vector Search
        embedding = self.embeddings.embed_query(self.query)
        vector_query = VectorizedQuery(vector=embedding, k_nearest_neighbors=50, fields="titleVector, descriptionVector, degreeNameVector, admissionRequirementVector, careerProspectVector", exhaustive=True)

        # 2. Retrieve the selected fields from the search index related to the question
        search_results = search_client.search(
            search_text=self.query, 
            vector_queries = [vector_query],
            top=5,
            select=["degreeCode", "title", "degree_name", "degree_type", "description", "admission_requirements","programme_duration","career_prospects"]
        )

        # 3. Initialize an empty list to hold formatted course information
        formatted_results = []
        
        for document in search_results:
            # Extract fields from the document, providing default values if necessary
            degree_info = {
                "score": document.get("@search.score", ""),
                "degreeCode": document.get("degreeCode", ""),
                "title": document.get("title", ""),
                "degree_name": document.get("degree_name", ""),
                "description": document.get("description", ""),
                "admission_requirements": document.get("admission_requirements", ""),
                "programme_duration": document.get("programme_duration", ""),
                "career_prospects": document.get("career_prospects", "")
            }
            
            formatted_results.append(degree_info)

        return formatted_results