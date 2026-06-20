# 📚🧠 Book Expert QA Bot

A Retrieval-Augmented Generation (RAG) powered document question-answering system built with Streamlit, ChromaDB, and Google Gemini.

The application allows users to upload and index PDF/DOCX documents, generate vector embeddings, retrieve relevant document chunks, and answer questions grounded in the indexed content.

---

# Features

* PDF document ingestion
* DOCX document ingestion
* Automatic text chunking
* Google Gemini Embeddings
* ChromaDB vector storage
* Semantic similarity search
* Retrieval-Augmented Generation (RAG)
* Streamlit web interface
* Source-aware document retrieval
* Metadata storage (source file and page number)
* Context-grounded question answering

---

# Technology Stack

| Component              | Technology             |
| ---------------------- | ---------------------- |
| UI                     | Streamlit              |
| LLM                    | Gemini 2.5 Flash Lite  |
| Embeddings             | Gemini Embedding Model |
| Vector Database        | ChromaDB               |
| PDF Parsing            | PyPDF                  |
| DOCX Parsing           | python-docx            |
| Environment Management | UV                     |
| Configuration          | python-dotenv          |

---

# Project Structure

```text
document-qa-bot/
│
├── data/
│   └── Input PDFs and DOCX files
│
├── db/
│   └── ChromaDB persistence directory
│
├── src/
│   ├── config.py
│   ├── ingest.py
│   ├── main.py
│   ├── query.py
│   ├── rag.py
│   └── __init__.py
│
├── .env
├── pyproject.toml
├── requirements.txt
├── uv.lock
│
├── RAG image-1.png
├── RAG image-2.png
│
└── README.md
```

---

# System Architecture

```text
Documents
    ↓
Ingestion Pipeline
    ↓
Chunking
    ↓
Gemini Embeddings
    ↓
ChromaDB Storage
    ↓
User Query
    ↓
Query Embedding
    ↓
Similarity Search
    ↓
Relevant Chunks
    ↓
Gemini LLM
    ↓
Answer Generation
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd document-qa-bot
```

---

# UV Setup

## Initialize Project

```bash
uv init
```

## Create Virtual Environment

```bash
uv venv
```

## Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

# Install Dependencies

Using UV:

```bash
uv sync
```

or

```bash
uv add streamlit chromadb google-genai pypdf python-docx python-dotenv
```

---

# Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=
DATABASE_LOCATION=
COLLECTION_NAME=
EMBEDDING_MODEL=
CHAT_MODEL=
```

Example:

```env
GEMINI_API_KEY=YOUR_API_KEY

DATABASE_LOCATION=./db/chroma_db

COLLECTION_NAME=qa_bot

EMBEDDING_MODEL=gemini-embedding-001

CHAT_MODEL=gemini-2.5-flash-lite
```

---

# Document Ingestion

Place your PDF or DOCX files inside:

```text
data/
```

Run ingestion:

```bash
cd src
python ingest.py
```

Expected output:

```text
Documents Indexed
Collection Count: XX
```

---

# Running the Application

Navigate to source directory:

```bash
cd src
```

Run Streamlit:

```bash
streamlit run main.py
```

Application will be available at:

```text
http://localhost:8501
```

---

# Retrieval Workflow

1. User enters a question.
2. Query is converted into a Gemini embedding.
3. ChromaDB performs similarity search.
4. Relevant document chunks are retrieved.
5. Retrieved chunks are provided to Gemini.
6. Gemini generates an answer grounded in the retrieved context.

---

# Screenshots

## Home Interface

![RAG Interface](RAG%20image-0.png)

---

## RAG Responses

![RAG Responses](RAG%20image-1.png)

---


![RAG Response](RAG%20image-2.png)

---

# Key Files

## ingest.py

Responsible for:

* Reading PDF and DOCX files
* Chunking document content
* Generating Gemini embeddings
* Storing vectors in ChromaDB

---

## query.py

Responsible for:

* Query embedding generation
* ChromaDB retrieval
* Context construction
* Gemini answer generation

---

## main.py

Responsible for:

* Streamlit UI
* Chat interface
* User interaction

---

## rag.py

Contains reusable RAG-related utilities and helper functions.

---

# Deployment

This application can be deployed on:

* Streamlit Community Cloud
* Render

Required deployment secrets:

```env
GEMINI_API_KEY
DATABASE_LOCATION
COLLECTION_NAME
EMBEDDING_MODEL
CHAT_MODEL
```

---

# Notes

This project uses Google Gemini APIs for both embeddings and answer generation.

The free Gemini tier has request and token limits. If embeddings or generation requests begin failing, you may have exhausted the available quota or encountered temporary rate limits.

For production workloads, consider using a paid Gemini plan or implementing request throttling and retry mechanisms.

---

# Author

Naveen Yarramsetti

App Link: https://bookexpertrag-5r26c3gxhmpjbfzybby4vp.streamlit.app/

Built using Streamlit, ChromaDB, and Google Gemini. 

