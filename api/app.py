from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with Vercel frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

# Load job vectors
with open("public/job_vectors.json", "r", encoding="utf-8") as f:
    job_data = json.load(f)

vectors = np.array([job["vector"] for job in job_data]).astype("float32")
metadata = job_data

# FAISS index
dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(vectors)

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

@app.post("/api/match")
async def match_jobs(req: QueryRequest):
    query_vec = model.encode([req.query]).astype("float32")
    distances, indices = index.search(query_vec, k=5)
    results = [metadata[i] for i in indices[0]]
    return results
