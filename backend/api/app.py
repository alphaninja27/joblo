from fastapi import FastAPI
import weaviate
from weaviate.client import WeaviateClient
from weaviate.classes.config import AdditionalConfig
from weaviate.classes.init import ConnectionParams, AuthApiKey
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

# Correct client connection setup
auth = AuthApiKey(api_key=WEAVIATE_API_KEY)
connection_params = ConnectionParams.from_params(
    http_host=WEAVIATE_URL,
    auth_client_secret=auth,
)

client = WeaviateClient(
    connection_params=connection_params,
    additional_config=AdditionalConfig(timeout=30)
)

@app.get("/")
def root():
    return {"status": "Weaviate backend running ✅"}
