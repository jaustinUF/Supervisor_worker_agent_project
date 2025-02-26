# "a little more sophisticated react (Reason and Act) agent ..."
from prompt_file import prompt_str
import re
import httpx
import openai
import os
from dotenv import load_dotenv
load_dotenv()       # load environmental variables
openai_api_key = os.getenv('OPENAI_API_KEY')

prompt = prompt_str
# "You run in a loop of Thought, Action, Observation, Answer."
# "Your available actions are:" calculate, wikipedia

# Instantiations of this class are ReAct agents!
#   Manages the conversation history, present updated history to the model, return models response
#   (https://chatgpt.com/c/67b4f7c0-bf88-800c-90c6-40e2c598cf27)
class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        self.client = openai.OpenAI(api_key = openai_api_key)

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        conversation = self.system + "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.messages]) # not used!?
        response = self.client.chat.completions.create(
            # model="gpt-3.5-turbo",
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.system},
                *self.messages
            ],
            max_tokens=1000,
            temperature=0
        )
        result = response.choices[0].message.content  # Accessing content using dot notation
        return result

# the agent returns a tool name and data/directions for the tool in the 'Action' return of the ReAct agent
action_re = re.compile(r'^Action: (\w+): (.*)$')        # regex pattern for valid 'Action:' return
# function to run the agent
# Accepts the user question, limits the number of reasoning loops, the prompt for the Chatbot object.
# see https://chatgpt.com/c/67b7a0a0-30e8-800c-9ee9-fa585e3e4dda for detail of agent/model - script communication
#   simple put: from 'Action', back through 'Observation
def query(question, max_turns=10, prompt=prompt):
    i = 0
    bot = ChatBot(system=prompt)                        # instantiate agent
    next_prompt = question
    while i < max_turns:                                # react loop count
        i += 1
        result = bot(next_prompt)
        # print(result)
        print(f'query result: {result}')
        # use 'action_re' pattern to make list of valid actions
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        if actions:                                     # action to perform?
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:             # tool not available?
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            # call the indicated function with proper input; assign return to 'observation'
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation) # tool return goes back to agent in 'Observation'
        else:                                           # no action, so model must have answer!
            return bot.messages # 'return' ends the function, and thus the loop!
            # this returns the complete conversation; could/should 'pull' the final answer out of text.


# 2 tools for the agent; referenced through the 'known_actions'dictionary'
def wikipedia(q):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]

def calculate(what):
    return eval(what)

known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate
}

answer = query("What is 20 * 15", prompt=prompt)
# answer = query("What languages are spoken in Spain that are also spoken in France")
# answer = query("Who are some billionaires from India that are also ranked as one of the richest people list in the world")
# answer = query("What is the longest river in the World?")

print(answer)