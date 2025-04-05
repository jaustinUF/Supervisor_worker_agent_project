from print_messages import prnt_msg
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from langchain.schema import OutputParserException
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')
load_dotenv()

model = ChatOpenAI(temperature=0, model="gpt-4o")
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
pdfs_directory = '../data/'
file_name = 'Employee Handbook (Sears).pdf'

# Helper functions
template = """
You are an assistant that answers questions. Using the following retrieved information, answer the user question. If you don't know the answer, say that you don't know. Use up to three sentences, keeping the answer concise.
Question: {question}
Context: {context}
Answer:
"""
def create_vector_store(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300, add_start_index=True)
    chunked_docs = text_splitter.split_documents(documents)
    return FAISS.from_documents(chunked_docs, embeddings)

def question_pdf(file_path, question):
    db = create_vector_store(file_path)
    docs = db.similarity_search(question, k=4)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"question": question, "context": context}).content

# Define the tool and agent
handbook_tool = Tool(
    name="employee_handbook_tool",
    func=lambda q: question_pdf(f"{pdfs_directory}{file_name}", q),
    description="Answers questions about the employee handbook PDF file."
)

employee_agent = create_react_agent(
    model=model,
    tools=[handbook_tool],
    name="employee_handbook_agent",
    prompt="You are an expert assistant for employee policy questions. Use the tool to answer questions about the employee handbook."
)

# Define the prompt to test the agent
prompt = "What is the employee pay rate on weekends?"
input_data = {
    "messages": [
        {"role": "user", "content": prompt}
    ]
}

# Run the agent with the provided input data
print(f"\nTesting Wikipedia Search with prompt: '{prompt}'\n")
try:
    response = employee_agent.invoke(input_data)
    # print(response)
    prnt_msg(response['messages'])
    # print(f"Response:\n{response['output']}\n")
    print(response["messages"][-1].content)
except OutputParserException as e:
    print(f"Parsing error encountered: {e}")
    # Define fallback behavior here
except Exception as e:
    print(f"An unexpected error occurred: {e}")