from jedi.inference.recursion import recursion_limit
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain.schema import OutputParserException
from print_messages import prnt_msg
import ast
import joblib
import numpy as np
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')
load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-4o")

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
            model = joblib.load(file)  # Using joblib instead of pickle
    except Exception as ex:
        raise ValueError(f"Error loading the model: {ex}")

    sample = np.array([features])
    prediction = model.predict(sample)
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
    model=llm,
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
## end predict agent

## create prompt for agent invoke
# prompt = (                                  # species: setosa
#     "Predict the species of an iris flower with sepal length 5.1, "
#     "sepal width 3.5, petal length 1.4, and petal width 0.2."
# )
# prompt = (                                  # species: virginica
#     "Predict the species of an iris flower with sepal length 6.3, "
#     "sepal width 3.3, petal length 6, and petal width 2.5."
# )
prompt = (                                # species: versicolor
    "Predict the species of an iris flower with sepal length 7, "
    "sepal width 3.2, petal length 4.7, and petal width 1.4."
)
input_data = {
    "messages": [
        {"role": "user", "content": prompt}
    ]
}
# invoke (run) the agent with the input request
print(f"\nTesting predictive agent with prompt: '{prompt}'\n")
try:
    response = predict_agent.invoke(input_data, config={"recursion_limit": 10})    # run (invoke agent
    # print(response)
    # prnt_msg(response['messages'])
    # print(f"Response:\n{response['output']}\n")
    print(response["messages"][-1].content)
except OutputParserException as e:
    print(f"Parsing error encountered: {e}")
    # Define fallback behavior here
except Exception as e:
    print(f"An unexpected error occurred: {e}")

#   [5.1, 3.5, 1.4, 0.2] # species: setosa
#   [7, 3.2, 4.7, 1.4]   # species: versicolor
#   [6.3, 3.3, 6, 2.5]  # species: virginica





