import json
import time 
import math
import streamlit as st
from .workflow.retrieval_workflow import Retrieval_Workflow
from pathlib import Path
from langfuse.callback import CallbackHandler
from dotenv import load_dotenv
from uuid import uuid4
from utils.Logger import setup_logger

load_dotenv(override=True)

def app_response(query: str, chat_id: str, cached_messages, user_profile: dict, user_id: str):
    """
    Invoke langgraph to generate coherent response back to users

    Attributes:
        query (str): Query by users
        chat_id (str): Unique chat uuid
        cached_messages (List[str]): A list of strings comprising of the previous query-response pair
        user_profile (dict): Dictionary that contains thes specific details of users
        user_id (str): Unique user ID
    
    Returns:
        response (str): Response generated by LLM
        run_id (str): Unique run ID
        status (str): Status of the generation response process
    
    Raises:
        Exception: If there are any errors
    """
    logging = setup_logger()
    logging.info("----------- Generating chatbot response ----------")
    # Define run_id
    run_id: str = str(uuid4())
    try:
        # Initialise Langfuse CallbackHandler for Langchain (tracing)
        langfuse_handler = CallbackHandler(session_id=chat_id, user_id=user_id)
        current_dir = Path(__file__).parent
        sub_dir = current_dir.parent/"ui"
        # Load Agent Explanation Json file 
        with open(f'{sub_dir}/agents_explanation.json', 'r') as file:
            agent_explanation = json.load(file)

        results = []
        workflow = Retrieval_Workflow().workflow_function()
        i=0
        # Create an expander for the detailed outputs
        with st.status("Generating responses...", expanded=True) as status:
            # Store starting time
            begin = time.time()
            for s in workflow.stream(
                {
                    "query": [query],
                    "cached_messages": cached_messages,
                    "user_profile": user_profile
                }, config={"run_id": run_id,
                        "callbacks": [langfuse_handler], 
                        "metadata": {
                            "langfuse_session_id": chat_id,
                            "predefined_run_id": run_id
                        }}
            ):
                if "__end__" not in s:
                    print(s)
                    print("------------------")
                    
                    for key in s.keys():
                        agent_caption = agent_explanation.get(key, None)
                        st.write(f"Step {i+1}: {key}:")
                        st.caption(agent_caption)
                        if 'generate_final_answer' in s:
                            results.append(s['generate_final_answer']['answer'])
                
                i += 1
            
            end = time.time()
            elapsed_time = math.ceil(end - begin)
            status.update(
                label=f"Thought for {elapsed_time} seconds", state="complete", expanded=False
            )
        
        return {"status": "success", "response": results[-1], "run_id": run_id}
    except Exception as e:
        logging.error("Unexpected Error while generating chatbot response")
        print(f"Error: {e}")
        return {
            "status": "error",
            "message": "f{e}: Unexpected Error while generating chatbot response",
            "run_id": run_id
        }
