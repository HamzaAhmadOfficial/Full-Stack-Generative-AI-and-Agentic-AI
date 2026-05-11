from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Vector Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embeddings,
)

# Take user input
user_query = input("Ask something: ")

# Relevant chunks from the vector db
search_results = vector_db.similarity_search(query=user_query)

context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number:{result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])


SYSTEM_PROMPT = f"""
 You are a helpful AI Assitant who answers user query based on the available context retrieved from a PDF file along with page_contents and page number,

 you should answer the user based on the following context and navigate the user to open the right page number to knoe more.

 context:
 {context}
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content":user_query },
    ]
)

print(f"RAG RESPONSE: {response.choices[0].message.content}")