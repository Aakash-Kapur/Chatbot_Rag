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


while (True):
    question = str(input("Enter you question: "))
    if question == "quit":
        break

    chat_history.append(HumanMessage(content=question))

    response = chatbot.invoke(chat_history)
    chat_history.append(AIMessage(content=response.content))


#while (True):
    #question = str(input("Enter your question: "))
    #if question == "quit":
    #    break

    #config = {"configurable": {"session_id": "session 1"}}

    #response = runnable.invoke(
    #[HumanMessage(content=question)],
    #config=config)

    #print(response.content)

    #chat_history.append(HumanMessage(content=question))
    #response = chatbot.invoke(chat_history)

    #chat_history.append(AIMessage(content=response.content))


class person():
    def __init__(self, name, age):
        self.name = name
        self.age = age


p1 = person('Aakash', 19)


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

sys_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant, answer all questions taking the person of {persona} to the best of your ability in {language}. "),
        MessagesPlaceholder(variable_name="input_msg"),
    ]
)

chain = sys_prompt | chatbot

new_runnable = RunnableWithMessageHistory(chain, get_msg_history, input_messages_key="input_msg")

#array = []

new_configurable = {"configurable": {"session_id": "random_session_id"}}

cur_response = new_runnable.invoke(
    {"input_msg": [HumanMessage(content="Hi there, how are you? ")],
     "language": "French",
     "persona": "pirate"},
    config=new_configurable
)

#array.extend([HumanMessage(content="Hi there, how are you? "), AIMessage(content=cur_response.content)])
