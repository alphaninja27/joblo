import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from weaviate.client import WeaviateClient
from weaviate.connect import ConnectionParams

load_dotenv()

# Environment Variables
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

# ✅ FIXED: Corrected from `from_parameters` to `from_params`
client = WeaviateClient(
    connection_params=ConnectionParams.from_params(
        http_host=WEAVIATE_URL,
        http_port=443,
        http_secure=True,
        auth_credentials={"apiKey": WEAVIATE_API_KEY}
    )
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class MatchRequest(BaseModel):
    query: str

@app.post("/api/match")
async def match_jobs(req: MatchRequest):
    result = client.collections.get("Job").query.bm25(
        query=req.query,
        limit=5,
        properties=["title", "company", "location", "skills", "url"]
    )
    return {"results": [obj.properties for obj in result.objects]}
