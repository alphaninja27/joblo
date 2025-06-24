import os
import json
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

# Load model and vectors
model = SentenceTransformer("all-MiniLM-L6-v2")
with open("public/job_vectors.json", "r") as f:
    job_data = json.load(f)
job_vectors = np.array([job["embedding"] for job in job_data], dtype="float32")

app = FastAPI()

class Query(BaseModel):
    query: str

# Cosine similarity
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

@app.post("/api/match")
def match(q: Query):
    q_vec = model.encode(q.query, convert_to_numpy=True).astype("float32")
    scores = [cosine_similarity(q_vec, vec) for vec in job_vectors]
    top_idxs = np.argsort(scores)[::-1][:5]
    results = []
    for idx in top_idxs:
        job = job_data[idx].copy()
        job["score"] = scores[idx]
        results.append(job)
    return results
