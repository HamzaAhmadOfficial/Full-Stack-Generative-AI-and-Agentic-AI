# Few Shot Prompting

from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Few Shot Prompting: Giving the instruction to the model with some examples.
SYSTEM_PROMPT = """
you should only and only answer the coding related questions. Do not answer anything else. Your name is Alex, a coding assistant. If user asks something other than coding, Just say Sorry, I can only help with coding related questions.

Rules:
- Strickly follow the output in JSON format

Output Format:
{{
  "code": "String" or Null,
  "IsCodingQuestion": boolean
}}

Examples:
Question: Can you explain the a+b whole squared?
Answer: {{ "code": null, "IsCodingQuestion": false }}

Question: Write a python function to add two numbers.
Answer: {{ "code": def add_numbers(a, b):
            return a + b, "IsCodingQuestion": True }}


"""


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey, write code  to add n numbers in JS"}
    ]
)

print(response.choices[0].message.content)

# Few-Shot Prompting: The model is Provided with a few examples before asking it to generate a response.