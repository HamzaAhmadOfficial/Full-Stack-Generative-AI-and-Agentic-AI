from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

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

def main():
    user_query = input("> ")
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", #Groq model
        messages=[
            {"role": "user", "content": user_query}

        ],
        temperature=0.7, # controls creativity of the response
        max_tokens=500 # limits the length of the response
    )

    print(f"Response: {response.choices[0].message.content}")


print(get_weather("goa"))