from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated
from typing_extensions import TypedDict
import streamlit as st


# LLM
llm = ChatOllama(model='llama3.1:8b-instruct-q4_1',
                 temperature=0,
                 num_predict = 1000,
                 keep_alive='12h')

def call_model(state: MessagesState):
    print('\nCurrent state:')
    print(state["messages"])
    response = llm.invoke(state["messages"])
    print("\nDeveloper-friendly response of the LLM:")
    print(response)

    return {"messages": response}


# TESTA GIT PUSH REPO BRANCHNAME VS GIT PUSH ORIGIN BRANCHNAME!

# Define the graph
builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_edge(START, "call_model")

# Set the checkpointer
checkpointer = MemorySaver()

# Build the graph
graph = builder.compile(checkpointer=checkpointer) # If you're using LangGraph Cloud or LangGraph Studio, you don't need to pass the checkpointer when compiling the graph, since it's done automatically.

# Set the thread
config = {"configurable": {"thread_id": "1"}}

# Set the title
st.write("# LangGraph implementation of a simple Chatbot with Cache Memory")

# Interact with the chatbot
go_on = True
counter=0
while go_on==True:
    counter = counter + 1
    user_input_1 = st.text_input("Ask me anything:", key=counter)
    input_message = {"type": "user", "content": user_input_1}    
    for chunk in graph.stream({"messages": [input_message]}, config, stream_mode="values"):
        st.write(chunk["messages"][-1].content)    

    counter = counter + 1
    user_input_2 = st.text_input("Do you want to ask me anything else? (y/n)", key=counter)
        
    if user_input_2 == 'n':
        go_on = False