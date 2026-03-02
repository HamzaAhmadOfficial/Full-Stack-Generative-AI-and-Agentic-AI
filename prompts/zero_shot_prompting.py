# Zero Shot Prompting

from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Zero Shot Prompting: Directly giving the instruction to the model without any examples.
SYSTEM_PROMPT = "you should only and only answer the coding related questions. Do not answer anything else. Your name is Alex, a coding assistant. If user asks something other than coding, Just say Sorry, I can only help with coding related questions."

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey, Can you write a python code to translate the word hello to urdu"}
    ]
)

print(response.choices[0].message.content)

# Zero-Shot Prompting: The model is given a direct question or task without any prior examples.