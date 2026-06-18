import chromadb
import google.generativeai as genai
from config import GEMINI_API_KEY
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_LOCATION = os.getenv("DATABASE_LOCATION")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
CHAT_MODEL = os.getenv("CHAT_MODEL")

client = chromadb.PersistentClient(
    path=DATABASE_LOCATION
)

collection = client.get_collection(
    COLLECTION_NAME
)

def search(query):
    results = collection.query(
        query_texts=[query],
        n_results=3,
        include=["documents","distances"]
    )
    return results



genai.configure(api_key=GEMINI_API_KEY)  # Here connection LLM MOdel

model = genai.GenerativeModel(
    CHAT_MODEL
)

def ask_question(question): # GENERATING ANSWERS HERE WITH OUR LLM GEMINI

    results = search(question)
    context = "\n\n".join(
        results["documents"][0]
    )
    prompt = f"""
    You are a document QA assistant.
    Answer ONLY using the provided context.
    If the answer is not explicitly present in the context,
    reply exactly:
    "I cannot find the answer in the provided documents."
    Context:
    {context}
    Question:
    {question}
    """
    response = model.generate_content(prompt)

    return response.text