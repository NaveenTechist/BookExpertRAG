import os
import uuid
import chromadb
from pathlib import Path
from pypdf import PdfReader
from docx import Document
BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv
from google import genai

load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"

DATABASE_LOCATION = os.getenv("DATABASE_LOCATION")
if DATABASE_LOCATION and not os.path.isabs(DATABASE_LOCATION):
    DATABASE_LOCATION = str((BASE_DIR / DATABASE_LOCATION).resolve())
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

print("INGEST STARTED")
print("DATA_DIR =", DATA_DIR)
print("DB =", DATABASE_LOCATION)
print("COLLECTION =", COLLECTION_NAME)

client_ai = genai.Client(api_key=GEMINI_API_KEY)

db = chromadb.PersistentClient(path=DATABASE_LOCATION)

collection = db.get_or_create_collection(
    name=COLLECTION_NAME
)

if collection.count() > 0:
    print(
        f"Collection already exists with "
        f"{collection.count()} documents"
    )
    exit()


def extract_pdf(file_path):
    pages = []


    reader = PdfReader(file_path)

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
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


def chunk_text(text, chunk_size=1000, overlap=200):
    if not text:
        return []
    words = text.split()
    chunks = []
    current_words = []
    current_char_count = 0
    for word in words:
        current_words.append(word)
        current_char_count += len(word) + (1 if current_char_count > 0 else 0)
        if current_char_count >= chunk_size:
            chunks.append(" ".join(current_words))
            overlap_words = []
            overlap_chars = 0
            for w in reversed(current_words):
                w_len = len(w) + (1 if overlap_chars > 0 else 0)
                if overlap_chars + w_len <= overlap:
                    overlap_words.insert(0, w)
                    overlap_chars += w_len
                else:
                    break
            if len(overlap_words) == len(current_words):
                overlap_words = overlap_words[1:]
                overlap_chars = sum(len(w) + (1 if idx > 0 else 0) for idx, w in enumerate(overlap_words))
            current_words = overlap_words
            current_char_count = overlap_chars
    if current_words:
        chunks.append(" ".join(current_words))
    return chunks


def create_chunks(pages):
    chunk_docs = []


    for page in pages:

        for chunk in chunk_text(page["text"]):

            chunk = chunk.strip()

            if len(chunk) < 10:
                continue

            chunk_docs.append({
                "text": chunk,
                "metadata": page["metadata"]
            })

    return chunk_docs


def embed_text(text):
    response = client_ai.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return response.embeddings[0].values


def save_chunks(chunks):
    ids = []
    docs = []
    metas = []
    embeddings = []

    for chunk in chunks:

        ids.append(str(uuid.uuid4()))
        docs.append(chunk["text"])
        metas.append(chunk["metadata"])

        embeddings.append(
            embed_text(chunk["text"])
        )

    collection.add(
        ids=ids,
        documents=docs,
        metadatas=metas,
        embeddings=embeddings
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
    print("Collection Count:", collection.count())

