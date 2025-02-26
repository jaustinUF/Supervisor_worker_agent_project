import datetime
from langchain.agents import tool

@tool
def check_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current date and time in the specified format"""

    # note: this discription is used by LLM to understand what this agent does!

    # Note that 'format' is a parameter with the indicated default
    #    Caller (AI) could specify format.
    # get the current date and time
    current_time = datetime.datetime.now()
    
    # format the time as a string in the format "YYYY-MM-DD HH:MM:SS"
    formatted_time = current_time.strftime(format)
    # print(f'formatted time = {formatted_time}')
    # return the formatted time
    return formatted_time