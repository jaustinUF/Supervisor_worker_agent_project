from tabnanny import verbose

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Note: LLM can be changed, but all 'AI' objects (like 'embeddings') must use same framework
# https://chatgpt.com/c/67c35b64-4874-800c-a044-77a2b6a5c564
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(temperature=0, model="gpt-4o")

pdfs_directory = 'pdfs/'                                # directory for pdf file, loaded though streamlit
embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b") # instantiate vectorization model
model = OllamaLLM(model="deepseek-r1:1.5b")             # LLM that will search the Un-vectorized text for the question
template = """
You are an assistant that answers questions. Using the following retrieved information, answer the user question. If you don't know the answer, say that you don't know. Use up to three sentences, keeping the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""

def upload_pdf(file):                                   # used by streamlit load pdf into 'pdfs' directory
    with open(pdfs_directory + file.name, "wb") as f:
        f.write(file.getbuffer())

def create_vector_store(file_path):                     # create/return vector db
    loader = PyPDFLoader(file_path)
    documents = loader.load()                           # get text from pdf
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300,
        add_start_index=True
    )

    chunked_docs = text_splitter.split_documents(documents) # chunk text
    db = FAISS.from_documents(chunked_docs, embeddings, verbose=False) # put vectorized chunks into database
    return db


def retrieve_docs(db, query, k=4):
    # print(db.similarity_search(query))
    return db.similarity_search(query, k)


def question_pdf(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    return chain.invoke({"question": question, "context": context})
