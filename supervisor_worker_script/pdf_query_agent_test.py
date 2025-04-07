# combines pdf_query_agent_main.py and pdf_query_agent_save_db.py into one file
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
model = ChatOpenAI(temperature=0, model="gpt-4o")

pdfs_directory = 'data/'  # Directory where PDFs are stored
file_name = 'Employee Handbook (Sears).pdf'

vector_store_directory = 'data/vectorstores/'  # Directory where FAISS indices will be saved

# Ensure the vector store directory exists
os.makedirs(vector_store_directory, exist_ok=True)

TEMPLATE = """
You are an assistant that answers questions. Using the following retrieved information, answer the user question. If you don't know the answer, say that you don't know. Use up to three sentences, keeping the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""

def create_or_load_vector_store(file_path):
    """
    Creates or loads a FAISS vector store for the given PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        FAISS: The vectorized document database.
    """
    file_name = os.path.basename(file_path)  # Extract the filename
    vector_store_path = os.path.join(vector_store_directory, file_name.replace('.pdf', ''))

    # If the FAISS index already exists, load it
    if os.path.exists(vector_store_path):
        print(f"Loading existing FAISS index from {vector_store_path}...")
        return FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)

    print(f"Creating FAISS index for {file_name}...")

    # Load and process the PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300,
        add_start_index=True
    )

    chunked_docs = text_splitter.split_documents(documents)

    # Create the FAISS index and save it
    db = FAISS.from_documents(chunked_docs, embeddings)
    db.save_local(vector_store_path)  # Save for future queries
    return db


def retrieve_docs(db, query, k=4):
    """
    Retrieves relevant document chunks from the vector database.

    Args:
        db (FAISS): The FAISS vector store.
        query (str): The search query.
        k (int): Number of relevant chunks to retrieve.

    Returns:
        list: Retrieved document chunks.
    """
    return db.similarity_search(query, k)


def question_pdf(question, documents):
    """
    Uses an LLM to generate an answer based on retrieved documents.

    Args:
        question (str): The user's question.
        documents (list): List of retrieved document chunks.

    Returns:
        str: The model-generated answer.
    """
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(TEMPLATE)
    chain = prompt | model
    response = chain.invoke({"question": question, "context": context})
    return response.content


def pdf_query_agent(file_path, question):
    """
    Processes a given PDF and answers a query based on its content.

    Args:
        file_path (str): Path to the PDF file.
        question (str): The question to ask.

    Returns:
        str: The model's response.
    """
    db = create_or_load_vector_store(file_path)  # Load or create FAISS vector store
    related_documents = retrieve_docs(db, question)  # Retrieve relevant chunks
    answer = question_pdf(question, related_documents)  # Generate response
    return answer


response = pdf_query_agent(pdfs_directory + file_name, 'What is the employee pay rate on weekends?')
# response = pdf_query_agent(pdfs_directory + file_name, 'What is the employee pay rate on holidays?')
print(response)
