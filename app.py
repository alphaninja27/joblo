from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import os

# Load the job vectors and metadata
with open("public/job_vectors.json", "r") as f:
    job_data = json.load(f)

job_vectors = np.array([job["embedding"] for job in job_data], dtype="float32")
metadata = [job["metadata"] for job in job_data]

# Load model once during startup
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create FastAPI app
app = FastAPI()

# Enable CORS (for Vercel or any other frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["https://your-vercel-app.vercel.app"] for stricter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API route for matching
@app.post("/api/match")
async def match_jobs(request: Request):
    body = await request.json()
    query = body.get("query", "")

    if not query:
        return []

    # Embed the user query
    query_vector = model.encode([query])[0]

    # Compute cosine similarities
    scores = job_vectors @ query_vector / (
        np.linalg.norm(job_vectors, axis=1) * np.linalg.norm(query_vector)
    )

    # Sort and get top 5
    top_indices = np.argsort(scores)[::-1][:5]
    results = [
        {
            **metadata[i],
            "score": float(scores[i])
        }
        for i in top_indices
    ]

    return results
