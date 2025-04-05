# put in try-except block to see errors
from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain.schema import OutputParserException
from print_messages import prnt_msg
import httpx
import warnings
from dotenv import load_dotenv
load_dotenv()       # load environmental variables
warnings.filterwarnings('ignore')

model = ChatOpenAI(temperature=0, model="gpt-4o")

## agents
# PDF search
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
pdfs_directory = 'data/'
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

# Tavily agent
tavily_tool = TavilySearchResults(max_results=2)
tavi_agent = create_react_agent(
    model=model,
    tools=[tavily_tool],
    name="tavi_agent",
    prompt="You are a web search expert. Use the Tavily tool to answer current or recent questions."
)

# Wikipedia agent
def wikipedia(q):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]

wikipedia_tool = Tool(
    name="wikipedia_search",
    func=wikipedia,
    description="Search Wikipedia and return the snippet from the first search result."
)

wiki_agent = create_react_agent(
    model=model,
    tools=[wikipedia_tool],
    name="wiki_agent",
    prompt="You are a Wikipedia expert. Use the Wikipedia Search tool to find reliable background information."
)

## Create supervisor workflow
workflow = create_supervisor(
    [employee_agent, wiki_agent, tavi_agent],
    model=model,
    prompt=(
        "You are a team supervisor managing an employee handbook search agent, a wikipedia search agent, and a web search agent."
        "For questions and information about employee rules and regulations, use employee_agent  . "
        "For general information, use wiki_agent."
        "To search the web, use tavi_agent."
    )
)

## Compile workflow
app = workflow.compile()
input_data = {
    "messages": [
        {
            "role": "user",
            # "content": "What is the employee pay rate on weekends?"
            # "content": "What is the area of Florida in square miles??"
            # "content": "What languages are spoken in Spain that are also spoken in France?"
            "content": "Search for the latest advancements in AI research."
        }
    ]
}
# invoke (run)
try:
    response = app.invoke(input_data)
    # print(response)
    # prnt_msg(response['messages'])
    # print(f"Response:\n{response['output']}\n")
    print(response["messages"][-1].content)
except OutputParserException as e:
    print(f"Parsing error encountered: {e}")
    # Define fallback behavior here
except Exception as e:
    print(f"An unexpected error occurred: {e}")