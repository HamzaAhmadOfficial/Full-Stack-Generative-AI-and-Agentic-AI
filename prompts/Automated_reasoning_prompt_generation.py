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

print("\n\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

user_query = input(" User:")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages=message_history,
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("Starting the process", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("Planning:", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("Final Output:", parsed_result.get("content"))
        break

print("\n\n\n")