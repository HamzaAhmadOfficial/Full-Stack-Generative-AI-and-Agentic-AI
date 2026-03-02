# Chain Of Thought Prompting

from dotenv import load_dotenv
from openai import OpenAI
import json

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

SYSTEM_PROMPT = """
    You're an expert AI assistant in resoving user queries using chain of thought
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strickly Folloe the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple time) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

    Example:
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
    
    

"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey, write a code to add n numbers in JS"},

        # Manually keep adding messages to History based on the responses
        {"role": "assistant", "content": json.dumps({"step": "PLAN", "content": "The user wants a JavaScript function to add 'n' numbers. I should create a function that can accept multiple numbers or an array of numbers and return their sum."})},
        {"role": "assistant", "content": json.dumps({"step": "PLAN", "content": "I need to write a JavaScript function that can add an arbitrary number of arguments. The best way to achieve this in modern JavaScript is by using rest parameters (`...args`). I will then use the `reduce` array method to sum all the numbers."})}
    ]
)

print(response.choices[0].message.content)