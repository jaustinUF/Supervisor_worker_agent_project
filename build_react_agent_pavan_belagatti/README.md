
reAct_AI_agent.py: "... more sophisticated agent" (6:24)
    - basic agent/tool interaction in the ReAct process (Thought, Act, and Observation):
        - agent 'calls' tool through 'Action:' step 
        - agent gets tools response back through the 'Observation' step
    - one agent: instantiated from class ChatBot
    - tutorial does not do an indepth discussion of this script.
    - my notes and ChatGPT session URLs in the script
    - detailed discussion of how agent 'calls' tool and receives response:
        'Agen/model interaction with Python script' (https://chatgpt.com/c/67b7a0a0-30e8-800c-9ee9-fa585e3e4dda)

structured_chat_agent.py: search the web agent
    - tool: Tavily Search Engine "Tavily is a search engine optimized for LLMs, aimed at efficient, quick and persistent search results."
                https://app.tavily.com/home
    - prompt: pulled from 'https://smith.langchain.com/hub'
    - changed llm to gpt-4o ... better answer

From Colab notebook: My Drive > Agent work > Examples/tutorials > 
        Structured-Chat-Agent.ipynb & ReAct-AI-Agent.ipynb (two scripts)
Build AI Agents (ReAct Agent) From Scratch Using LangChain!
https://www.youtube.com/watch?v=VoWGD4mvKjU
m