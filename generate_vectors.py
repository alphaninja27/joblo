from sentence_transformers import SentenceTransformer
import numpy as np
import json
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

job_descriptions = [
    {
        "title": "Senior Software Engineer",
        "company": "Acme Corp",
        "location": "Remote",
        "description": "Backend development using Python and Django.",
        "url": "https://example.com/job1"
    },
    {
        "title": "Frontend Developer",
        "company": "Beta Ltd",
        "location": "Bangalore",
        "description": "React, TypeScript, and CSS expertise needed.",
        "url": "https://example.com/job2"
    },
    {
        "title": "Data Scientist",
        "company": "DataWorks",
        "location": "Remote",
        "description": "Machine learning, Python, and SQL.",
        "url": "https://example.com/job3"
    },
    {
        "title": "DevOps Engineer",
        "company": "InfraCloud",
        "location": "Delhi",
        "description": "AWS, Docker, CI/CD pipelines experience.",
        "url": "https://example.com/job4"
    },
    {
        "title": "Full Stack Developer",
        "company": "TechGen",
        "location": "Remote",
        "description": "Node.js, React, and MongoDB.",
        "url": "https://example.com/job5"
    }
]

# Prepare text for embeddings
texts = [f"{job['title']} at {job['company']}. {job['description']}" for job in job_descriptions]
vectors = model.encode(texts, convert_to_numpy=True)

# Construct the final structure
data = [
    {
        "embedding": vector.tolist(),
        "metadata": job
    }
    for job, vector in zip(job_descriptions, vectors)
]

# Ensure public/ directory exists
os.makedirs("public", exist_ok=True)

# Save to public/job_vectors.json
with open("public/job_vectors.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ job_vectors.json created successfully.")
