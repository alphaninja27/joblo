from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import faiss
import numpy as np
import cohere

# Load environment
from dotenv import load_dotenv
load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load job data
with open("public/job_vectors.json", "r") as f:
    job_data = json.load(f)

texts = [job["text"] for job in job_data]
metadata = [job["metadata"] for job in job_data]

# Generate FAISS index
dimensions = 384  # Cohere embeds to 768-dim vectors


index = faiss.IndexFlatL2(dimensions)

vectors = np.array([job["embedding"] for job in job_data]).astype("float32")
index.add(vectors)

class Query(BaseModel):
    query: str

@app.post("/api/match")
async def match(query: Query):
    response = co.embed(
        texts=[query.query],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    query_vector = np.array(response.embeddings[0]).astype("float32").reshape(1, -1)
    distances, indices = index.search(query_vector, k=5)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx])
    return results
