from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "you are an expert in Maths and only answer maths related questions. If the question is not related to maths, Just say sorry and do not answer that."},
#        {"role": "user", "content": "Hey, I am Hamza Ahmad! Nice to meet you. Who are you?"}
#        {"role": "user", "content": "Hey, can you code a python that can print hello world?"}
        {"role": "user", "content": "Hey, Can you help me solve the a + b whole squared?"}
    ]
)

print(response.choices[0].message.content)