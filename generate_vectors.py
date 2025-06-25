from sentence_transformers import SentenceTransformer
import numpy as np
import json
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

jobs = [
    {
        "title": "Senior Software Engineer",
        "company": "TechCorp",
        "location": "Remote",
        "description": "Senior Software Engineer with experience in backend development using Python and Django.",
        "url": "https://example.com/job1"
    },
    {
        "title": "Frontend Developer",
        "company": "DesignPro",
        "location": "Bangalore",
        "description": "Frontend Developer with strong skills in React, TypeScript, and CSS.",
        "url": "https://example.com/job2"
    },
    {
        "title": "Data Scientist",
        "company": "DataWiz",
        "location": "Remote",
        "description": "Data Scientist role requiring experience in machine learning, Python, and SQL.",
        "url": "https://example.com/job3"
    },
    {
        "title": "DevOps Engineer",
        "company": "DeployHub",
        "location": "Mumbai",
        "description": "DevOps Engineer with knowledge of AWS, Docker, and CI/CD pipelines.",
        "url": "https://example.com/job4"
    },
    {
        "title": "Full Stack Developer",
        "company": "BuildIt",
        "location": "Hyderabad",
        "description": "Full Stack Developer proficient in Node.js, React, and MongoDB.",
        "url": "https://example.com/job5"
    }
]

descriptions = [job["description"] for job in jobs]
embeddings = model.encode(descriptions, convert_to_numpy=True)

job_data = []
for job, emb in zip(jobs, embeddings):
    job["embedding"] = emb.tolist()
    job_data.append(job)

os.makedirs("public", exist_ok=True)
with open("public/job_vectors.json", "w") as f:
    json.dump(job_data, f, indent=2)

print("✅ job_vectors.json created with embeddings.")
