import requests
import json

def search_jobs(prompt):
    res = requests.post("https://joblo-1bvy.onrender.com/api/match", json={"query": prompt})
    if res.ok:
        jobs = res.json()
        if not jobs:
            print("❌ No matching jobs found.")
            return
        print("\n✅ Top Matching Jobs:\n")
        for i, job in enumerate(jobs, 1):
            print(f"{i}. {job['title']} at {job['company']} ({job['location']})")
            print(f"   🔗 {job['url']}\n")
    else:
        print("❌ API Error:", res.status_code)

if __name__ == "__main__":
    query = input("🔍 Enter your job query: ")
    search_jobs(query)
