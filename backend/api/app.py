from fastapi import FastAPI
import os
from dotenv import load_dotenv
from weaviate import WeaviateClient
from weaviate.classes.init import AuthApiKey, ConnectionParams

load_dotenv()

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

auth = AuthApiKey(api_key=WEAVIATE_API_KEY)

connection_params = ConnectionParams.from_params(
    http_host=WEAVIATE_URL,
    auth_client_secret=auth,
)

client = WeaviateClient(connection_params=connection_params)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is working 🎉"}
