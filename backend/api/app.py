from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import weaviate
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load your Weaviate config
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://your-weaviate-instance.weaviate.network")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

# Initialize Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class MatchRequest(BaseModel):
    query: str

# Setup Weaviate client
client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY),
    additional_headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")},
)

@app.post("/api/match")
def match_jobs(req: MatchRequest):
    query = req.query
    query_embedding = model.encode(query).tolist()

    response = client.query.get("Job", ["title", "company", "description", "link"]).with_near_vector({
        "vector": query_embedding
    }).with_limit(5).do()

    results = response["data"]["Get"]["Job"]
    return {"results": results}
