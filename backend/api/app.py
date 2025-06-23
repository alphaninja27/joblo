import os
import weaviate

WEAVIATE_URL = os.getenv("kc2zvxratigq8ekck04yq.c0.asia-southeast1.gcp.weaviate.cloud")       # e.g. "my-cluster.something.weaviate.cloud"
WEAVIATE_API_KEY = os.getenv("MkhxL2NkYWtKVXBSTnFHRF9HUTFPNU4wbWtBem1NRmlYNjhmdWlpUms1eEx5VFRSVHA1Y0o3MTYxR0VVPV92MjAw")  # may be empty if local

if WEAVIATE_API_KEY:
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=weaviate.classes.init.Auth.api_key(WEAVIATE_API_KEY),
        headers={}  # add any extra headers if needed
    )
else:
    # Connect to a local / self-hosted endpoint
    client = weaviate.connect_to_custom(
        http_host=WEAVIATE_URL,
        http_port=8080,
        http_secure=WEAVIATE_URL.startswith("https"),
        grpc_host=WEAVIATE_URL,
        grpc_port=50051,
        grpc_secure=WEAVIATE_URL.startswith("https"),
    )

assert client.is_ready(), "Weaviate client is not ready"
