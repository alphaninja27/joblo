from sentence_transformers import SentenceTransformer
import json
import os

INPUT_FILE = "public/jobs.json"
OUTPUT_FILE = "public/job_vectors.json"

model = SentenceTransformer("all-MiniLM-L6-v2")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    jobs = json.load(f)

job_vectors = []
for job in jobs:
    text = f"{job['title']} at {job['company']}. {job['description']}"
    vector = model.encode(text).tolist()
    job_vectors.append({
        "title": job["title"],
        "company": job["company"],
        "location": job.get("location", ""),
        "description": job["description"],
        "url": job.get("url", ""),
        "vector": vector
    })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(job_vectors, f, indent=2)

print("✅ job_vectors.json generated successfully.")
