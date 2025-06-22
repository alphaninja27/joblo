from sentence_transformers import SentenceTransformer
from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams
import re

# Known skills for fuzzy matching
KNOWN_SKILLS = ["python", "sql", "react", "aws", "javascript", "flask", "css", "django"]

def extract_keywords(prompt):
    words = prompt.lower().split()
    skills = [word for word in words if word in KNOWN_SKILLS]
    location = None
    if "bangalore" in prompt.lower():
        location = "Bangalore"
    return skills, location

def embed(text):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(text)

def search(prompt):
    vector = embed(prompt)

    client = WeaviateClient(
        connection_params=ConnectionParams.from_url("http://localhost:8080", grpc_port=50051)
    )
    client.connect()
    collection = client.collections.get("Job")

    results = collection.query.near_vector(near_vector=vector, limit=5)

    client.close()
    return results.objects

def display_results(jobs):
    if not jobs:
        print("\n❌ No matching jobs found. Try being more general.")
        return

    print("\n✅ Top Job Matches:")
    for job in jobs:
        j = job.properties
        print(f"\n📌 {j['title']} at {j['company']}")
        print(f"   📍 {j['location']}")
        print(f"   💡 Skills: {', '.join(j['skills'])}")
        print(f"   🔗 {j['url']}")

if __name__ == "__main__":
    prompt = input("🤖 BuddyBot CLI\nWhat kind of job are you looking for?\n> ")
    matches = search(prompt)
    display_results(matches)
