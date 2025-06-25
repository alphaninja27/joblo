from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import numpy as np
import json, os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def load_vectors():
    global job_data, embeddings, model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    with open("public/job_vectors.json") as f:
        job_data = json.load(f)
    embeddings = np.array([j['embedding'] for j in job_data], dtype="float32")

@app.post("/api/match")
async def match(query: dict):
    q = query.get("query","")
    q_emb = model.encode([q], convert_to_numpy=True)[0]
    sims = embeddings.dot(q_emb) / (np.linalg.norm(embeddings,axis=1)*np.linalg.norm(q_emb))
    topk = sims.argsort()[-5:][::-1]
    return [job_data[i] for i in topk]
