from langchain_community.document_loaders import WebBaseLoader # webpage loader
from langchain_text_splitters import RecursiveCharacterTextSplitter # chunker
from langchain_chroma import Chroma # vector database
from langchain_ollama import OllamaEmbeddings

loader = WebBaseLoader(web_path="https://ninjago.fandom.com/wiki/Lloyd") # loader object of class WebBaseLoader
text = loader.load() # stores text from webage

chunker = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50, add_start_index=True) # chunker object of class RCT
chunks = chunker.split_documents(text) # text but in chunked form

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector_database = Chroma(
    embedding_function=embeddings,
    persist_directory="./vb_dir"
)

vector_database.add_documents(documents=chunks)
#print(type(vector_database))
