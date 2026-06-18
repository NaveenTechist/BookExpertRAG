import os
from pypdf import PdfReader
from docx import Document
from dotenv import load_dotenv
import chromadb
from pathlib import Path
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATABASE_LOCATION = os.getenv("DATABASE_LOCATION")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = chromadb.PersistentClient(
    path=DATABASE_LOCATION
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

def extract_pdf(file_path):
    pages = []

    reader = PdfReader(file_path)

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            pages.append({
                "text": text,
                "metadata": {
                    "source": os.path.basename(file_path),
                    "page": page_num
                }
            })

    return pages


def extract_docx(file_path):
    doc = Document(file_path)

    text = "\n".join(
        para.text for para in doc.paragraphs
    )

    return [{
        "text": text,
        "metadata": {
            "source": os.path.basename(file_path),
            "page": 1
        }
    }]

def chunk_text(text, chunk_size=1000, overlap=200): # here this is chunking function

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks    

def create_chunks(pages):  # Here Doc into chunks

    chunk_docs = []

    for page in pages:
        chunks = chunk_text(page["text"])
        for chunk in chunks:
            chunk_docs.append({
                "text": chunk,
                "metadata": page["metadata"]
            })
    return chunk_docs

def save_chunks(chunks):

    ids = []
    docs = []
    metas = []

    for i, chunk in enumerate(chunks):

        ids.append(str(i))
        docs.append(chunk["text"])
        metas.append(chunk["metadata"])

    collection.add(
        ids=ids,
        documents=docs,
        metadatas=metas
    )

if __name__ == "__main__":

    pages = []

    for file in os.listdir(DATA_DIR):
        path = DATA_DIR / file
        if file.endswith(".pdf"):
            pages.extend(extract_pdf(path))
        elif file.endswith(".docx"):
            pages.extend(extract_docx(path))
    chunks = create_chunks(pages)
    save_chunks(chunks)

    print("Documents Indexed")