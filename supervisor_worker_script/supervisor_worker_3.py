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
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002") # instantiate factorizing object from class
pdfs_directory = 'data/'
file_name = 'Employee Handbook (Sears).pdf'

# Helper functions
template = """
You are an assistant that answers questions. Using the following retrieved information, answer the user question. If you don't know the answer, say that you don't know. Use up to three sentences, keeping the answer concise.
Question: {question}
Context: {context}
Answer:
"""
def create_vector_store(file_path):                         # function to create vectorized db
    loader = PyPDFLoader(file_path)                         # instantiate loader object from class
    documents = loader.load()                               # load PDF into list of documents (e.g. PDF page)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300, add_start_index=True) # instantiate splitter object from class
    chunked_docs = text_splitter.split_documents(documents) # split into overlapping 'chunks' (to preserve context across sections)
    return FAISS.from_documents(chunked_docs, embeddings)   # vectorize chunks and store in memory 'vector store'

def question_pdf(file_path, question):                      # function to search PDF for information
    db = create_vector_store(file_path)                     # create vectorized db
    docs = db.similarity_search(question, k=4)              # Find most relevant four chunks
    context = "\n\n".join([doc.page_content for doc in docs]) # extract text (which should be 'answer')
    prompt = ChatPromptTemplate.from_template(template)     # put question and context into prompt template (defined above)
    chain = prompt | model                                  # 'pipe' prompt to model
    # invoke model after the chain formats the prompt using 'question' and 'context' values
    return chain.invoke({"question": question, "context": context}).content # response; should be 'answer' to 'question'

# Define the tool and agent
handbook_tool = Tool(                                       # search PDF for information
    name="employee_handbook_tool",
    func=lambda q: question_pdf(f"{pdfs_directory}{file_name}", q), # link search function to tool
    description="Answers questions about the employee handbook PDF file."
)

employee_agent = create_react_agent(
    model=model,
    tools=[handbook_tool],                                  # 'give' tool to agent
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

## Create and compile supervisor workflow
workflow = create_supervisor(
    [employee_agent, wiki_agent, tavi_agent],
    model=model,
    prompt=(
        "You are a team supervisor managing an employee handbook search agent, a wikipedia search agent, and a web search agent."
        "For questions and information about employee rules and regulations, use employee_agent. "
        "For general information, use wiki_agent."
        "To search the web, use tavi_agent."
    )
)
app = workflow.compile()
input_data = {
    "messages": [
        {
            "role": "user",
            "content": "What is the employee pay rate on weekends?"
            # "content": "What is the area of Florida in square miles??"
            # "content": "What languages are spoken in Spain that are also spoken in France?"
            # "content": "Search for the latest advancements in AI research."
        }
    ]
}
## invoke (run) compiled workflow
try:
    response = app.invoke(input_data)
    # print(response)                               # complete messages thread
    # prnt_msg(response['messages'])                # formatted messages thread
    print(response["messages"][-1].content)         # answer to question
except OutputParserException as e:
    print(f"Parsing error encountered: {e}")
    # Define fallback behavior here
except Exception as e:
    print(f"An unexpected error occurred: {e}")