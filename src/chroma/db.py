import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
import os
import uuid
from dotenv import load_dotenv

# load env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# define ef of database
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-ada-002"
)

# define db
client = chromadb.Client(
    Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./cache",
    )
)
giglet_ai_collection = client.get_or_create_collection("giglet_ai", embedding_function=openai_ef)

def gen_random_id():
    return str(uuid.uuid4())

def remember(text):
    """Remember a question and answer pair in the database."""
    giglet_ai_collection.add(
        ids=[gen_random_id()],
        documents=[text]
    )

def recall(query: str, n: int):
    """Recall the top n most similar question and answer pairs to the query."""
    results = giglet_ai_collection.query(
        query_texts=[query],
        n_results=n
    )
    return results['documents'][0]
