from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams
from transformers import AutoTokenizer, AutoModel
import torch

app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def get_embedding(text: str) -> list:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().tolist()


# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/match")
async def match(request: Request):
    data = await request.json()
    query = data.get("query", "")

    client = WeaviateClient(
        connection_params=ConnectionParams.from_url("http://localhost:8080", grpc_port=50051)
    )
    client.connect()

    vector = model.encode(query)
    collection = client.collections.get("Job")

    results = collection.query.near_vector(near_vector=vector, limit=5)
    jobs = [obj.properties for obj in results.objects]

    client.close()
    return jobs
