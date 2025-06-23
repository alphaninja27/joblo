# backend/api/app.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import weaviate

load_dotenv()

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

if not WEAVIATE_URL:
    raise RuntimeError("Missing WEAVIATE_URL env var")

# Correct v4 client init
client = weaviate.WeaviateClient(
    url=WEAVIATE_URL,
    auth=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY) if WEAVIATE_API_KEY else None
)

# Test connection
if not client.is_ready():
    raise RuntimeError("Weaviate instance not reachable or not ready.")

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok", "weaviate": True}
