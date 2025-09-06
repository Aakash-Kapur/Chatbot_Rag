import ollama, os
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import OllamaEmbeddings
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_core.messages import AIMessage, HumanMessage
from langsmith import Client

# Initialize LangSmith client

# Set up LangSmith environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"
LANGCHAIN_PROJECT = "rag-pipeline-tracing"

client = Client()

# Initialize chatbot and other variables
chatbot = ChatOllama(model="phi3.5")
sys_messge = """You are an assistant for question-answering tasks. '
'ONLY use the following pieces of retrieved context to answer '
'the question; absolutely nothing else from the internet or any other sources.'
'If the answer is not in the context, say you do not know.'
'Use three sentences maximum and keep you answer concise.'
'The aforementioned retrieved context is below: '
'\n\n'
'{context}'"""

llm_array = []
found_starting_llm = False
cur_persona = "helpful assistant"
starting_msg = "Hello, I am your local ChatBot. To quit the program, view all created conversations, or switch between chatbots, simply type 'quit', 'menu', 'switch', or 'persona' respectively when asked to enter a question. "
persona_msg = "Enter a persona for the ChatBot (e.g., pirate, police officer, financial advisor). Enter 'D' for a default ChatBot: "
chat_history = []

context_message = """You will be given a chat history and a current question.
It is highly likely that the current question will require you to consult the chat history
which is a record of everything
that you can make referGiven a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

while True:
    if len(llm_array) == 0:
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

    if question != "switch" and question != "quit":
        sys_prompt = ChatPromptTemplate.from_messages(
            [("system", sys_messge),
             MessagesPlaceholder(variable_name="chat_history"),
             ("human", "{input}"),
             ]
        )

        context_prompt = ChatPromptTemplate.from_messages(
            [("system", context_message),
             MessagesPlaceholder(variable_name="chat_history"),
             ("human", "{input}")
             ]
        )

        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vector_database = Chroma(
            embedding_function=embeddings,
            persist_directory="./vb_dir"
        )

        # Create the retrieval chain
        history_retriever = create_history_aware_retriever(chatbot, vector_database.as_retriever(), context_prompt)
        docs_chain = create_stuff_documents_chain(chatbot, sys_prompt)
        retrieval_chain = create_retrieval_chain(retriever=history_retriever, combine_docs_chain=docs_chain)

        # Invoke the retrieval chain (LangSmith will automatically trace this)
        response = retrieval_chain.invoke({"input": question, "persona": cur_persona, "chat_history": chat_history})

        # Update chat history
        cur_qn = HumanMessage(content=question)
        cur_ans = AIMessage(content=response['answer'])
        chat_history.extend([cur_qn, cur_ans])
        print(cur_ans.content)
        question = str(input("Enter question: "))
        