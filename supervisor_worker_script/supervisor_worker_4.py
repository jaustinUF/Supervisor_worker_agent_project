# similar to supervisor_worker_3.py. Three agents: PDF search, Wikipedia search, Iris species predictor
from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import OutputParserException
from print_messages import prnt_msg
import httpx
import numpy as np
import ast
import joblib
import warnings
from dotenv import load_dotenv
load_dotenv()       # load environmental variables
warnings.filterwarnings('ignore')

model = ChatOpenAI(temperature=0, model="gpt-4o")

### agents
## PDF search
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

def question_pdf(file_path, question):                      # tool function: search PDF for information
    db = create_vector_store(file_path)                     # create vectorized db
    docs = db.similarity_search(question, k=4)              # Find most relevant four chunks
    context = "\n\n".join([doc.page_content for doc in docs]) # extract text (which should be 'answer')
    template_prompt = ChatPromptTemplate.from_template(template)     # put question and context into prompt template (defined above)
    chain = template_prompt | model                                  # 'pipe' prompt to model
    # invoke model after the chain formats the prompt using 'question' and 'context' values
    return chain.invoke({"question": question, "context": context}).content # response; should be 'answer' to 'question'

# Define the tool and agent
handbook_tool = Tool(                           # Create tool: search PDF for information
    name="employee_handbook_tool",
    func=lambda q: question_pdf(f"{pdfs_directory}{file_name}", q), # link search function to tool
    description="Answers questions about the employee handbook PDF file."
)

employee_agent = create_react_agent(
    model=model,
    tools=[handbook_tool],                      # 'give' tool to agent
    name="employee_handbook_agent",
    prompt="You are an expert assistant for employee policy questions. Use the tool to answer questions about the employee handbook."
)

## begin predict agent
# tool function
def predict_func(features: list[float]):
    target_names = ['setosa', 'versicolor', 'virginica']
    model_path = "iris_model.pkl"

    # Ensure the input is a proper list of floats
    if isinstance(features, str):
        try:
            features = ast.literal_eval(features)
        except Exception:
            raise ValueError(f"Invalid input format. Expected list of floats, got: {features}")

    if not isinstance(features, list) or len(features) != 4:
        raise ValueError(
            "Expected a list of four numerical values: [sepal length, sepal width, petal length, petal width].")

    try:                                        # load model
        with open(model_path, 'rb') as file:
            ml_model = joblib.load(file)  # Using joblib instead of pickle
    except Exception as ex:
        raise ValueError(f"Error loading the model: {ex}")

    sample = np.array([features])
    prediction = ml_model.predict(sample)
    return target_names[prediction[0]]
# create tool
predict_tool = Tool(
    name='predict_tool',
    func=predict_func,
    description=(                               # for the agent llm, not the tool ML model
        "Use this tool to predict the species of an iris flower. "
        "Pass four numerical values as a list (not a string). "
        "Format: [5.1, 3.5, 1.4, 0.2]"
    )
)
# create agent
predict_agent = create_react_agent(
    model=model,
    tools=[predict_tool],
    name= 'predict_agent',
    prompt= (
        "You are an expert in identifying iris flower species. "
        "When the user gives sepal and petal measurements, "
        "use the 'predict_tool' to predict the species. "
        "First extract the four numbers: sepal length, sepal width, petal length, petal width, "
        "then call the tool with these values as a list of float values."
    )
)

## Wikipedia agent
def wikipedia(q):                               # tool function
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]

wikipedia_tool = Tool(                          # create tool
    name="wikipedia_search",
    func=wikipedia,                             # assign function to tool
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
    [employee_agent, wiki_agent, predict_agent],
    model=model,
    prompt=(
        "You are a team supervisor managing an employee handbook search agent, a wikipedia search agent, and a Iris species predictor."
        "For questions and information about employee rules and regulations, use employee_agent. "
        "For general information, use wiki_agent."
        "To predict an Iris species from septal and pedal measurements, use predict_agent."
    )
)
app = workflow.compile()

## create prompt for supervisor agent invoke
# prompt = "What is the employee pay rate on weekends?"
# prompt = "What is the area of Florida in square miles?"
# prompt = "What are the species of the Iris flower plant?"
prompt = "List the ten most popular species of the Iris flower plant?"
# prompt = "What languages are spoken in Spain that are also spoken in France?"
# species: setosa
# prompt = "Predict the species of an iris flower with sepal length 5.1, sepal width 3.5, petal length 1.4, and petal width 0.2."
# species: virginica
# prompt = "Predict the species of an iris flower with sepal length 6.3, sepal width 3.3, petal length 6, and petal width 2.5."
# species: versicolor
# prompt = "Predict the species of an iris flower with sepal length 7, sepal width 3.2, petal length 4.7, and petal width 1.4."
# species: versicolor
# prompt = "Predicted species of iris flower with these measurements: 6.3, 3.3, 4.7, 1.6"
# prompt = "Species of iris flower with these measurements: 6.3, 3.3, 4.7, 1.6"

input_data = {
    "messages": [
        {"role": "user", "content": prompt}
    ]
}
print(f"\nRequest or question: '{prompt}'\n")
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

