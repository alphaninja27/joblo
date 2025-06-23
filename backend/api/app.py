import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import weaviate
from dotenv import load_dotenv

load_dotenv()

# Initialize Weaviate client
client = weaviate.Client(
    url=os.getenv("WEAVIATE_URL"),
    auth_client_secret=weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY")),
)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class MatchRequest(BaseModel):
    query: str

@app.post("/api/match")
async def match_jobs(req: MatchRequest):
    # Simple GraphQL search: filter where title, description or skills contains query
    filter_body = {
        "operator": "Or",
        "operands": [
            {"path": ["title"], "operator": "Contains", "valueString": req.query},
            {"path": ["description"], "operator": "Contains", "valueString": req.query},
            {"path": ["skills"], "operator": "Contains", "valueString": req.query},
        ]
    }

    result = client.query.get("Job", ["title", "company", "location", "skills", "url"]) \
        .with_where(filter_body) \
        .with_limit(5) \
        .do()

    return {"results": result["data"]["Get"]["Job"]}
