from sentence_transformers import SentenceTransformer
from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams
import uuid

# Sample jobs
jobs = [
    {
        "title": "Backend Engineer",
        "company": "TechCorp",
        "location": "Bangalore",
        "skills": ["python", "sql", "aws"],
        "description": "Design and develop APIs using Python and AWS.",
        "url": "https://techcorp.com/jobs/123"
    },
    {
        "title": "Frontend Developer",
        "company": "UIX Labs",
        "location": "Remote",
        "skills": ["react", "javascript", "css"],
        "description": "Build beautiful user interfaces with React.",
        "url": "https://uixlabs.com/jobs/456"
    }
]

# Initialize embedder
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Weaviate
client = WeaviateClient(
    connection_params=ConnectionParams.from_url("http://localhost:8080", grpc_port=50051)
)
client.connect()

collection = client.collections.get("Job")

for job in jobs:
    text = f"{job['title']} {job['description']} {' '.join(job['skills'])}"
    vector = model.encode(text)

    collection.data.insert(
        uuid=uuid.uuid4(),
        properties=job,
        vector=vector
    )

print("✅ Seeded sample job listings.")
client.close()
