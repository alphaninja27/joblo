from sentence_transformers import SentenceTransformer
from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams

# Initialize embedder
model = SentenceTransformer("all-MiniLM-L6-v2")

# User query (can replace this with resume text or CLI input)
query = input("🔍 Enter job query or resume text:\n> ")

query_vector = model.encode(query)

# Connect to Weaviate
client = WeaviateClient(
    connection_params=ConnectionParams.from_url("http://localhost:8080", grpc_port=50051)
)
client.connect()

collection = client.collections.get("Job")

# Search top 5 semantically closest
results = collection.query.near_vector(
    near_vector=query_vector,
    limit=5
)

print("\n🎯 Top Matching Jobs:")
for job in results.objects:
    props = job.properties
    print(f"\n📌 {props['title']} at {props['company']}")
    print(f"   📍 {props['location']}")
    print(f"   🔗 {props['url']}")
    print(f"   💡 Skills: {', '.join(props['skills'])}")
    print(f"   📝 {props['description']}")

client.close()
