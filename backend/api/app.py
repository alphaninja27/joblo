from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams

app = FastAPI()
model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

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
