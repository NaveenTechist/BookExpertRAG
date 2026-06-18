from dotenv import load_dotenv
import os
load_dotenv()


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_LOCATION = str(
    BASE_DIR / "db" / "chroma_db"
)



DATABASE_LOCATION = os.getenv("DATABASE_LOCATION")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")