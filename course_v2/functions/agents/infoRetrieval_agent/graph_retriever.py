import os 
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from neo4j.exceptions import CypherSyntaxError
from langchain_neo4j.chains.graph_qa.cypher_utils import CypherQueryCorrector, Schema
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Neo4jVector
from langchain_core.prompts import ChatPromptTemplate
from functions.utils.neo4j.graph_examples import graph_few_shot_examples
from functions.models.agent_types import ValidateCypherOutput
from functions.models.graph_states import OverallState, OutputState

load_dotenv(override=True)

class GraphRetrieval:
    def __init__(self):
        self.NEO4J_URI = os.getenv('NEO4J_URI')
        self.NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
        self.NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
        self.NEO4J_DATABASE = os.getenv('NEO4J_DATABASE')
        self.graph = Neo4jGraph(url = self.NEO4J_URI, username = self.NEO4J_USERNAME, password = self.NEO4J_PASSWORD, database = self.NEO4J_DATABASE)
        self.graph.refresh_schema()
        self.enhanced_graph = Neo4jGraph(enhanced_schema=True)
        self.enhanced_graph.refresh_schema()
        # print(self.enhanced_graph.schema)
        self.llm = AzureChatOpenAI(model="gpt-4o-mini-lke")
        self.llm_4o = AzureChatOpenAI(model="ANV2Exp-AzureOpenAI-NorthCtrlUS-TWY-GPT4o")
        self.azure_embeddings = AzureOpenAIEmbeddings(
                azure_deployment=os.environ.get('TEXT_EMBEDDING_MODEL_DEPLOYMENT'),
                api_key = os.environ.get('AZURE_OPENAI_APIKEY'),
                azure_endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT'),
                model = os.environ.get('TEXT_EMBEDDING_MODEL_NAME')
            )
        # Cypher query corrector functions
        self.corrector_schema = [
            Schema(el["start"], el["type"], el["end"])
            for el in self.enhanced_graph.structured_schema.get("relationships")
        ]
        self.cypher_query_corrector = CypherQueryCorrector(self.corrector_schema)
    # Utils Function
    def generate_cypher(self,query: str):
        examples = graph_few_shot_examples()
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples, 
            self.azure_embeddings,
            Neo4jVector, 
            k=5,
            input_keys=["question"]
        )

        text2cypher_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Given an input question, convert it to a Cypher query. No pre-amble"
                        "Do not wrap the response in any backticks or anything else. Respond with a Cypher statement only!"

                    ),
                ),
                (
                    "human",
                    (
                        """
                        You are a Neo4j expert. Given an input question, create a syntactically correct Cypher query to run.
                        Do not wrap the response in any backticks or anything else. Respond with a Cypher statement only! 
                        Here is the schema information
                        {schema}

                        Below are a number of examples of qeustions and their corresponding Cypher queries. If the question is similar, you should refrain from changing the provided Cypher queries, and generate the exact same Cypher query.

                        {fewshot_examples}

                        User input: {question}
                        Cypher query:
                        """
                    )
                )
            ]
        )

        text2cypher_chain = text2cypher_prompt | self.llm | StrOutputParser()
        
        NL  = "\n"
        fewshot_examples = (NL * 2).join(
            [
                f"Question: {el['question']}{NL}Cypher:{el['query']}"
                for el in example_selector.select_examples(
                    {"question": query}
                )
            ]
        )

        generated_cypher = text2cypher_chain.invoke(
            {
                "question": query, 
                "fewshot_examples": fewshot_examples, 
                "schema": self.enhanced_graph.schema
            }
        )

        return generated_cypher   
    
    def validate_cypher(self):
        validate_cypher_system = """
                You are a Cypher expert reviewing a statement written by a junior developer. 
                                 """
        
        validate_cypher_user = """
                You must check the following:
                * Are there any syntax errors in the Cypher statement?
                * Are there any missing or undefined variables in the Cypher statement?
                * Are any node labels missing from the schema?
                * Are any relationship types missing from the schema? 
                * Are any of the properties not included in the schema?
                * Does the Cypher statement include enough information to answer the question?

                Examples of good errors:
                * Label (:Foo) does not exist, did you mean (:Bar)?
                * Property bar does not exist for label Foo, did you mean baz?
                * Relationship FOO does not exist, did you mean FOO_BAR?

                Examples of Property Filters:
                {{
                    "question": "How many math related courses are compulsory for a Computer Science (CSC) student.",
                    "query": "MATCH (c:Course)-[:HAS_TYPE]->(t: Type {{typeName: 'Core'}})  MATCH (c)-[:OFFERED_BY]->(d: Degree {{degreeCode: 'CSC'}}) WHERE c.scope = 'MATH' OR c.courseCode STARTS WITH 'MH' RETURN COUNT(c)",
                    "filters": "filters=[Property(node_label='Course', property_key='scope', property_value='MATH'), Property(node_label='Type', property_key='typeName', property_value='Core'), Property(node_label='Degree', property_key='degreeCode', property_value='CSC')]"
                }}

                Schema:
                {schema}

                The question is: 
                {question}

                The Cypher statement is:
                {cypher}

                Make sure you don't make any mistakes! 
                               """
        
        validate_cypher_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    validate_cypher_system,
                ),
                (
                    "human",
                    (validate_cypher_user)
                )
            ]
        )

        validate_cypher_chain = validate_cypher_prompt | self.llm_4o.with_structured_output(ValidateCypherOutput)

        return validate_cypher_chain
    
    def correct_cypher(self):
        correct_cypher_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are a Cypher expert reviewing a statement written by a junior developer. "
                        "You need to correct the Cypher statement based on the provided errors. No pre-amble."
                        "Do not wrap the response in any backticks or anything else. Respond with a Cypher statement only!"
                    ),
                ),
                (
                    "human",
                    (
                        """Check for invalid syntax or semantics and return a corrected Cypher statement.

                        Schema:
                        {schema}

                        Note: Do not include any explanations or apologies in your responses.
                        Do not wrap the response in any backticks or anything else.
                        Respond with a Cypher statement only!

                        Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.

                        The question is:
                        {question}

                        The Cypher statement is:
                        {cypher}

                        The errors are:
                        {errors}

                        Corrected Cypher statement: """
                    ),
                ),
            ]

        )

        correct_cypher_chain = correct_cypher_prompt | self.llm_4o | StrOutputParser()

        return correct_cypher_chain
    
    def generate_final_answer(self):
        generate_final_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant",
                ),
                (
                    "human",
                    (
                        """Use the following results retrieved from a database to provide succint, definitive answer to the user's question.
                        
                        Respond as if you are answering the question directly. 

                        Results: {results}
                        Question: {question}
                        """
                    ),
                ),
            ]
        )

        generate_final_chain = generate_final_prompt | self.llm_4o | StrOutputParser()

        return generate_final_chain

    # Node functions
    def generate_cypher_node(self, state: OverallState) -> OverallState: 
        """
        Generate a cypher statement based on the provided schema and user input
        """
        query = state.get('query')[-1]
        generated_cypher = self.generate_cypher(query)

        return {
            "cypher_statement": generated_cypher, 
            "steps": ["generate_cypher"]
            }
    
    
    def validate_cypher_node(self,state: OverallState) -> OverallState:
        """
        Validates the Cypher statements and maps any property values to the database
        """
        errors = []
        mapping_errors = []
        # Check for syntax errors
        try:
            self.enhanced_graph.query(f"EXPLAIN {state.get('cypher_statement')}")
        except CypherSyntaxError as e:
            print(e.message)
            errors.append(e.message)
        
        # Experimental feature for correcting relationship directions
        # corrected_cypher = self.cypher_query_corrector(state.get("cypher_statement"))
        # if not corrected_cypher:
        #     errors.append("The generated Cypher statement doesn't fit the graph schema")
        # if not corrected_cypher == state.get("cypher_statement"):
        #     print("Relationship direction was corrected")

        # Use LLM to find additional potential errors and get the mapping for values
        # print("Corrected Cypher: ", corrected_cypher)
        # print("Original Cypher: ", state.get("cypher_statement"))
        # validate_cypher_chain = self.validate_cypher()
        # llm_output = validate_cypher_chain.invoke(
        #     {
        #         "question": state.get("query")[-1],
        #         "schema": self.graph.schema, 
        #         "cypher": state.get("cypher_statement")
        #     }
        # )

        # # print(llm_output)

        # if llm_output.errors:
        #     errors.extend(llm_output.errors)
        # if llm_output.filters:
        #     for filter in llm_output.filters:
        #         # Do mapping only for string values
        #         # Collect all matching props
        #         matching_props = [
        #             prop
        #             for prop in self.enhanced_graph.structured_schema["node_props"].get(
        #                 filter.node_label, []
        #             )
        #             if prop["property"] == filter.property_key
        #         ]
        #         # print(matching_props)

        #         # If not matching property is found, skip
        #         if not matching_props:
        #             continue 

        #         # Check the property type 
        #         if matching_props[0]["type"] != "STRING":
        #             continue
                
        #         mapping = self.enhanced_graph.query(
        #             f"MATCH (n:{filter.node_label}) WHERE toLower(n.`{filter.property_key}`) = toLower($value) RETURN 'yes' LIMIT 1",
        #             {"value": filter.property_value},
        #         )

        #         # print(mapping)
                
        #         if not mapping:
        #             print(
        #                 f"Missing value mapping for {filter.node_label} on property {filter.property_key} with value {filter.property_value}"
        #             )
        #             mapping_errors.append(
        #                 f"Missing value mapping for {filter.node_label} on property {filter.property_key} with value {filter.property_value}"
        #             )
        
        if mapping_errors:
            next_action = "end"
        elif errors:
            next_action = "correct_cypher"
        else:
            next_action = "execute_cypher"
        # print("Corrected Cypher: ", corrected_cypher)
        # if not corrected_cypher:
        #     return {
        #     "next_action": next_action, 
        #     "cypher_statement": state.get("cypher_statement"),
        #     "cypher_errors": errors, 
        #     "steps": ["validate_cypher"]
        # }
        return {
            "next_action": next_action, 
            "cypher_statement": state.get("cypher_statement"),
            "cypher_errors": errors, 
            "steps": ["validate_cypher"]
        }
    
    def correct_cypher_node(self, state:OverallState) -> OverallState: 
        """
        Correct the Cypher statement based on the provided errors.
        """

        correct_cypher_chain = self.correct_cypher()
        corrected_cypher = correct_cypher_chain.invoke(
            {
                "question": state.get("query")[-1],
                "errors": state.get("cypher_errors"),
                "cypher": state.get("cypher_statement"),
                "schema": self.enhanced_graph.schema,
            }
        )

        return {
            "next_action": "validate_cypher",
            "cypher_statement": corrected_cypher,
            "steps": ["correct_cypher"]
        }
    
    def execute_cypher_node(self, state: OverallState) -> OverallState:
        """
        Executes the given Cypher statement.
        """
        no_results = "I couldn't find any relevant information in the database."

        try:
            records = self.enhanced_graph.query(state.get("cypher_statement"))
        except CypherSyntaxError as e:
            records = "I couldn't find any relevant information in the database."

        # print(records)
        
        return {
            "database_records": records if records else no_results,
            "next_action": "end",
            "steps": ["execute_cypher"]
        }
    
    def generate_final_answer_node(self, state:OverallState) -> OutputState:
        """
        Decides if the question is related to course planning.
        """
        generate_final_chain = self.generate_final_answer()
        final_answer = generate_final_chain.invoke(
            {"question": state.get("query")[-1], "results": state.get("database_records")}
        )

        return {
            "message": [final_answer],
            "answer": final_answer, 
            "steps": ["generate_final_answer"]
            }