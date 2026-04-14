from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
import json
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The current weather in {city} is {response.text}"
    
    return "Something went wrong"


available_tools = {
    "get_weather": get_weather
}


SYSTEM_PROMPT = """
    You're an expert AI assistant in resoving user queries using chain of thought
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call a tool if required from the list of available tools.
    For every tool call wait for the observe step which is the output from the called tool.

    Rules:
    - Strickly Folloe the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple time) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "Tool": "string", "input": "string" }

    Available Tools:
    - get_weather(city: str): Takes a city name as input string and returns the current weatehr information about the city.


    Example 1:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN": "Content": "Seems like user is interseted in math problem" }
    PLAN: { "step": "PLAN": "Content": "Looking at the problem, we should solve this using BODMAS method" }
    PLAN: { "step": "PLAN": "Content": "Yes, The BODMAS is correct thing to be done here" }
    PLAN: { "step": "PLAN": "Content": "first we do division 5 / 10 = 0.5 which is 0.5" }
    PLAN: { "step": "PLAN": "Content": "Now the new equation is 2 + 3 * 0.5" }
    PLAN: { "step": "PLAN": "Content": "then we do multiplication 3 * 0.5 = 1.5 which is 1.5" }
    PLAN: { "step": "PLAN": "Content": "Now the new equation is 2 + 1.5" }
    PLAN: { "step": "PLAN": "Content": "finally we do addition 2 + 1.5 = 3.5 which is 3.5" }
    PLAN: { "step": "PLAN": "Content": "Great, We have solved the problem and 3.5 as Answer" }
    OUTPUT: { "step": "OUTPUT", "content": "The answer to 2 + 3 * 5 / 10 is 3.5" }
    

    Example 2:
    START: What is the weather in Islamabad?
    PLAN: { "step": "PLAN": "Content": "Seems like user is interseted in getting weather of Islamabad in Pakistan" }
    PLAN: { "step": "PLAN": "Content": "Lets see if we have any available tool from the list of available tools" }
    PLAN: { "step": "PLAN": "Content": "Great, we have the get_weather tool available for this query" }
    PLAN: { "step": "PLAN": "Content": "I need to call the get_weather tool for Islamabad as input for city" }
    PLAN: { "step": "TOOL": "tool": "get_weather", "input": "Islamabad" }
    PLAN: { "step": "OBSERVE": "tool": "get_weather", "output": "The temperature of Islamabad is cloudy with 20 C" }
    PLAN: { "step": "PLAN": "Content": "Great, I got the weather info about Islamabad" }
    OUTPUT: { "step": "OUTPUT", "content": "The current weather in Islamabad is cloudy with 20 C" }
    

"""

print("\n\n\n")

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None, description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call.")
    input: Optional[str] = Field(None, description="The input params for the tool")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    user_query = input(" User👉:")
    message_history.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.parse(
            model="openai/gpt-oss-120b",
            response_format=MyOutputFormat,
            messages=message_history,

        )

        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result})

        parsed_result = response.choices[0].message.parsed

        if parsed_result.step == "START":
            print("Starting the process", parsed_result.content)
            continue

        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            print(f"Calling tool {tool_to_call} with input {tool_input}")

            tool_response = available_tools[tool_to_call](tool_input)
            print(f"Calling tool = {tool_to_call}, with input = {tool_input}, got response = {tool_response}")
            message_history.append({"role": "developer", "content": json.dumps(
                {"step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response}
            )})
            continue


        if parsed_result.step == "PLAN":
            print("Planning:", parsed_result.content)
            continue

        if parsed_result.step == "OUTPUT":
            print("Final Output:", parsed_result.content)
            break

print("\n\n\n")