# API Key: AIzaSyCJeId4uXLda0QiE0oDJHniwtnLackH9Hs

from langchain_ollama import ChatOllama
# langchain_ollama is similar to langchain_openai (subset of langchain) but contains the ollama non-api stuff
# ChatOllama is a class that is the 'interface' behind the chatbot

from langchain_core.messages import AIMessage, HumanMessage

chatbot = ChatOllama(model="phi3.5")
# ChatOllama is the chatbot interface and takes in human messages and outputs AI messages
# Ollama allows you to intefact with the LLM (phi3.5) directly and takes in strings and outputs strings


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


count = 1
id_array = []
cur_id = f"session {count}"
id_array.append(cur_id)


while (True):

    question = str(input("Enter your question: "))
    if question == "quit":
        break

    id_response = int(input(f"Enter which session id do want to navigate to: \nYou are currently on {cur_id} of {count}: "))

    if id_response == int(cur_id[-1]): # want to stay on current session number
        pass

    elif id_response < int(cur_id[-1]): # want to navigate to a previous session number
        if id_response < 1:
            print("Invalid previous session number!")
        else:
            cur_id = id_array[id_response - 1]

    elif id_response > int(cur_id[-1]) and id_response <= count: # want to navigate to a future session number thats already created 
        cur_id = id_array[id_response - 1]

    else: # want to create a a new session id
        count += 1
        cur_id = f"session {count}"
        id_array.append(cur_id)


    config = {"configurable": {"session_id": cur_id}}

    response = runnable.invoke(
    [HumanMessage(content=question)],
    config=config)

    print(response.content)


class person():
    def __init__(self, name, age):
        self.name = name
        self.age = age


p1 = person('Aakash', 19)
