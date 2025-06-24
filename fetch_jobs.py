import json
from pathlib import Path

# Simulated raw job listings from Naukri and company sites
raw_jobs = [
    {"title": "Software Engineer", "company": "TCS", "location": "Bangalore", "description": "Backend Python Developer.", "url": "https://tcs.com/jobs/123"},
    {"title": "Frontend Engineer", "company": "Infosys", "location": "Remote", "description": "React developer with strong UI skills.", "url": "https://infosys.com/jobs/456"},
    {"title": "Data Scientist", "company": "Naukri.com", "location": "Gurgaon", "description": "Experience with ML models.", "url": "https://naukri.com/viewjob?id=ds1"},
    {"title": "DevOps Engineer", "company": "Zoho", "location": "Chennai", "description": "Docker, Kubernetes, AWS.", "url": "https://zoho.com/careers/devops"},
    {"title": "Software Engineer", "company": "TCS", "location": "Bangalore", "description": "Backend Python Developer (Duplicate Entry).", "url": "https://tcs.com/jobs/duplicate"},
    {"title": "AI Researcher", "company": "Google", "location": "Hyderabad", "description": "Work on cutting-edge ML.", "url": "https://careers.google.com/jobs/ai"},
    {"title": "QA Tester", "company": "Flipkart", "location": "Bangalore", "description": "Manual + automation testing.", "url": "https://flipkartcareers.com/qa"},
    {"title": "Product Manager", "company": "Amazon", "location": "Remote", "description": "Experience in e-commerce domain.", "url": "https://amazon.jobs/pm"},
    {"title": "Security Analyst", "company": "Paytm", "location": "Noida", "description": "Security threat assessment.", "url": "https://paytm.com/careers/sec"},
    {"title": "Data Engineer", "company": "Reliance Jio", "location": "Mumbai", "description": "Big data pipelines.", "url": "https://careers.jio.com/dataeng"},
    {"title": "ML Engineer", "company": "Byju's", "location": "Bangalore", "description": "Model deployment experience.", "url": "https://byjus.com/careers/ml"},
    {"title": "Software Engineer", "company": "TCS", "location": "Bangalore", "description": "Backend Python Developer (Triplicate).", "url": "https://tcs.com/jobs/triple"},
]

# Deduplication logic (by title + company)
seen = set()
deduped = []

for job in raw_jobs:
    key = (job['title'].lower(), job['company'].lower())
    if key not in seen:
        seen.add(key)
        deduped.append(job)

# Output path
output_path = Path("public/jobs.json")
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w") as f:
    json.dump(deduped, f, indent=2)

print(f"✅ Fetched and deduplicated {len(deduped)} jobs. Saved to public/jobs.json")
