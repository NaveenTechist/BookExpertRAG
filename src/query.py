import chromadb
import os
from pathlib import Path
import subprocess
import chromadb
BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv
from google import genai

load_dotenv(BASE_DIR / ".env")

DATABASE_LOCATION = os.getenv("DATABASE_LOCATION")
if DATABASE_LOCATION and not os.path.isabs(DATABASE_LOCATION):
    DATABASE_LOCATION = str((BASE_DIR / DATABASE_LOCATION).resolve())
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
CHAT_MODEL = os.getenv("CHAT_MODEL")
INGEST_FILE = Path(__file__).parent / "ingest.py"

client_ai = genai.Client(api_key=GEMINI_API_KEY)

db = chromadb.PersistentClient(
    path=DATABASE_LOCATION
)

try:
    collection = db.get_collection(
        name=COLLECTION_NAME
    )

except Exception:

    print("Collection not found. Running ingest.py...")

    subprocess.run(
        ["python", str(INGEST_FILE)],
        check=True
    )

    collection = db.get_collection(
        name=COLLECTION_NAME
    )

def embed_query(query):
    response = client_ai.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query
    )

    return response.embeddings[0].values


def search(query):
    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )
    return results


def ask_question(question):
    results = search(question)

    context_parts = []
    if results and "documents" in results and results["documents"]:
        documents = results["documents"][0]
        metadatas = results.get("metadatas", [[]])[0] if results.get("metadatas") else []
        for i, doc in enumerate(documents):
            meta = metadatas[i] if i < len(metadatas) else {}
            source = meta.get("source", "Unknown")
            page = meta.get("page", "Unknown")
            context_parts.append(f"--- Chunk {i+1} [Source: {source}, Page: {page}] ---\n{doc}")
    
    context = "\n\n".join(context_parts)

    prompt = f"""You are a highly accurate document QA assistant.
Answer the user's question ONLY using the provided context chunks.
Do not assume, extrapolate, or use outside knowledge.
If the context does not contain the answer, reply exactly:
I cannot find the answer in the provided documents.

Context chunks:
{context}

Question: {question}
Answer:"""

    response = client_ai.models.generate_content(
        model=CHAT_MODEL,
        contents=prompt
    )

    return response.text

