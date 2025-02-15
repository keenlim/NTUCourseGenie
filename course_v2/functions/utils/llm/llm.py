import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

# Load environment variables
load_dotenv(override=True)

# OpenAI Models
def gpt_3_5_turbo_openai():
    return ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0)

def gpt_4o_mini_openai():
    return ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

def gpt_4o_openai():
    return ChatOpenAI(model_name="gpt-4o", temperature=0)

# Azure OpenAI Models
def gpt_4o_mini_azure():
    return AzureChatOpenAI(model="gpt-4o-mini-lke", temperature=0)

def gpt_4o_azure():
    return AzureChatOpenAI(model="ANV2Exp-AzureOpenAI-NorthCtrlUS-TWY-GPT4o", temperature=0)

def azure_text_embedding():
    return AzureOpenAIEmbeddings(
                azure_deployment = os.environ.get('TEXT_EMBEDDING_MODEL_DEPLOYMENT'),
                api_key = os.environ.get('AZURE_OPENAI_APIKEY'),
                azure_endpoint= os.environ.get('AZURE_OPENAI_ENDPOINT'),
                model= os.environ.get('TEXT_EMBEDDING_MODEL_NAME'),
            )



