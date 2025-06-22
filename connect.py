from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams

client = WeaviateClient(
    connection_params=ConnectionParams.from_url("http://localhost:8080", grpc_port=50051)
)

client.connect()

if client.is_ready():
    print("✅ Connected to Weaviate!")

    # List collection names
    existing_collections = [col.name for col in client.collections.list_all()]

    if "Job" not in existing_collections:
        client.collections.create_from_dict(
            {
                "class": "Job",
                "vectorIndexConfig": {
                    "distance": "cosine",
                    "vectorCacheMaxObjects": 100000
                },
                "properties": [
                    {"name": "title", "dataType": ["text"]},
                    {"name": "company", "dataType": ["text"]},
                    {"name": "location", "dataType": ["text"]},
                    {"name": "skills", "dataType": ["text[]"]},
                    {"name": "description", "dataType": ["text"]},
                    {"name": "url", "dataType": ["text"]}
                ]
            }
        )
        print("✅ Job schema created.")
    else:
        print("ℹ️ Job schema already exists.")
else:
    print("❌ Failed to connect.")

client.close()
