# API Key: AIzaSyCJeId4uXLda0QiE0oDJHniwtnLackH9Hs
import ollama
import streamlit as st
from langchain_ollama import ChatOllama
# langchain_ollama is similar to langchain_openai (subset of langchain) but contains the ollama non-api stuff
# ChatOllama is a class that is the 'interface' behind the chatbot
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chatbot = ChatOllama(model="phi3.5")
# ChatOllama is the chatbot interface and takes in human messages and outputs AI messages
# Ollama allows you to intefact with the LLM (phi3.5) directly and takes in strings and outputs strings

st.write("Hello there")
# response = chatbot.invoke(question) # .invoke allows the chatbot to receive a question and returns the answer

chat_history = []

my_dict = {}
#my_dict {"session1": chat_history_forses1, "sessin2",chathisorysessin2}

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

def get_msg_history(session_id):
    if session_id not in my_dict:
        my_dict[session_id] = InMemoryChatMessageHistory()
    return my_dict[session_id]

runnable = RunnableWithMessageHistory(chatbot, get_msg_history)



from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


id_array = []
llm_array = []
found_starting_llm = False
cur_persona = "helpful assistant"
starting_msg = "Hello, I am your local Chatbot. To quit the program, view all created conversations or switch between chatbots, simply type 'quit', 'menu', 'switch' or 'persona' respectively when asked to enter a question. "
persona_msg = "Enter a persona for the ChatBot (e.g. pirate, police officer, financial advisor). Enter 'D' for a default ChatBot: "

while (True):

    if len(id_array) == 0:
        print(starting_msg)

        while not found_starting_llm:
            try:
                cur_llm = str(input("Enter which ChatBot to use: "))
                ollama.pull(cur_llm)
                llm_array.append(cur_llm)
                chatbot = ChatOllama(model=cur_llm)
                break
            except:
                print("Invalid model! ")

        cur_sess = str(input("Enter first conversation name: "))
        id_array.append(cur_sess)

        entered_persona = str(input(persona_msg))
        if entered_persona == 'D':
            cur_persona = "helpful assistant"
        else:
            cur_persona = entered_persona

        question = str(input("Enter question: "))


    if question == "quit":
        print("Successfully quitted, have a nice day! ")
        break


    if question == "switch":
        for i in range(len(llm_array)):
            print(f"Model {i + 1} is {llm_array[i]}")

        while not found_starting_llm:
            try:
                cur_llm = str(input("Which ChatBot do you want to switch to? "))
                ollama.pull(cur_llm)
                if cur_llm not in llm_array:
                    llm_array.append(cur_llm)
                chatbot = ChatOllama(model=cur_llm)
                break
            except:
                print("Invalid model! ")

        question = str(input("Enter question: "))


    if question == "menu":
        for i in range(len(id_array)):
            print(f"Session {i + 1} is {id_array[i]}")

        id_input = str(input("Which session id to navigate to? "))
        if id_input not in id_array:
            id_array.append(id_input)
            
        cur_sess = id_input
        question = str(input("Enter question: "))


    if question == "persona":
        entered_persona = str(input(persona_msg))
        if entered_persona == 'D':
            cur_persona = "helpful assistant"
        else:
            cur_persona = entered_persona

        question = str(input("Enter question: "))


    if question != "switch" and question != "menu" and question != "quit" and question != "persona":

        sys_prompt = ChatPromptTemplate.from_messages(
        [("system", "You are a helpful assistant, answer all questions taking the persona of (a) {persona}. "),
         MessagesPlaceholder(variable_name="input_msg")]
         )

        chain = sys_prompt | chatbot
        new_runnable = RunnableWithMessageHistory(chain, get_msg_history, input_messages_key="input_msg")
        new_configurable = {"configurable": {"session_id": cur_sess}}
        
        cur_response = new_runnable.invoke(
            {"persona": cur_persona,
            "input_msg": [HumanMessage(content=question)]},
            config=new_configurable
        )
        
        print(cur_response.content)
        question = str(input("Enter question: "))
