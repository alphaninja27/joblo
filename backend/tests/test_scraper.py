import json
import os

def test_job_scraper_output():
    assert os.path.exists("public/jobs.json"), "❌ jobs.json not found"
    with open("public/jobs.json") as f:
        jobs = json.load(f)
    assert len(jobs) >= 20, "❌ Less than 20 jobs fetched"
    for job in jobs:
        assert "title" in job and "description" in job and "url" in job