import json
import time 
import math
import streamlit as st
from .workflow.retrieval_workflow import Retrieval_Workflow
from pathlib import Path

def app_response(query: str, chat_id: str, cached_messages, user_profile: dict):
    current_dir = Path(__file__).parent
    sub_dir = current_dir.parent/"ui"
    print(sub_dir)
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
            },
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
    
    return results[-1]
