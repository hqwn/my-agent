#Main file for building our AI Agent, and creating the function to call our AI Agent

# Basic imports for our AI Agent 
from dotenv import load_dotenv
from langchain.agents import create_agent
import os
from langchain_openai import ChatOpenAI
import os
from tools import tools_list

#Importing the system prompt
with open('./txt_files/system.txt', 'r') as file:
    system_prompt = file.read()


#The AI Agent setup
load_dotenv()

#Our main AI which we will use for our AI Agent, and creating our agent with langchain
llm = ChatOpenAI(
    #gpt-oss-20b this is base ai model what we are using
    model="openai/gpt-oss-120b:free", 
    api_key=os.getenv('HACK_CLUB_AI'),
    base_url="https://ai.hackclub.com/proxy/v1"
)
agent = create_agent(
    model=llm,
    tools= tools_list,
    system_prompt=system_prompt
)

#basic function to call our agent to test it
def ask_agent(prompt):
    result = agent.invoke({"messages": [{'role': 'user', 'content': prompt}]}, config={"recursion_limit": 15})
    return result["messages"][-1].content

#function which our UI will use to call agent
def ask_streamlit(history):

    result = agent.invoke(
        {"messages": history},
        config={"recursion_limit": 15}
    )

    return result["messages"][-1].content
