from weaviate import WeaviateClient
from weaviate.auth import AuthApiKey
import os

WEAVIATE_URL = os.getenv("kc2zvxratigq8ekck04yq.c0.asia-southeast1.gcp.weaviate.cloud")
WEAVIATE_API_KEY = os.getenv("MkhxL2NkYWtKVXBSTnFHRF9HUTFPNU4wbWtBem1NRmlYNjhmdWlpUms1eEx5VFRSVHA1Y0o3MTYxR0VVPV92MjAw")

if not WEAVIATE_URL:
    raise RuntimeError("Missing WEAVIATE_URL env variable")

auth = AuthApiKey(api_key=WEAVIATE_API_KEY) if WEAVIATE_API_KEY else None

client = WeaviateClient(
    weaviate_url=WEAVIATE_URL,
    auth_client=auth
)
