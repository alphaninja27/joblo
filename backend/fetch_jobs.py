import requests
from bs4 import BeautifulSoup
import json
import time
import random
import logging

logging.basicConfig(level=logging.INFO)

def fetch_linkedin_jobs():
    url = "https://www.linkedin.com/jobs/search/?keywords=python"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36'
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        # Placeholder logic; actual selectors may vary
        jobs = []
        for i, job_card in enumerate(soup.select(".job-card-container")):
            job = {
                "title": job_card.select_one(".job-card-list__title").get_text(strip=True) if job_card.select_one(".job-card-list__title") else "",
                "company": job_card.select_one(".job-card-container__company-name").get_text(strip=True) if job_card.select_one(".job-card-container__company-name") else "",
                "location": job_card.select_one(".job-card-container__metadata-item").get_text(strip=True) if job_card.select_one(".job-card-container__metadata-item") else "",
                "date": "N/A",
                "url": job_card.select_one("a")['href'] if job_card.select_one("a") else ""
            }
            jobs.append(job)
            if i == 4: break  # limit to 5 jobs

        return jobs
    except Exception as e:
        logging.error(f"Failed to fetch LinkedIn jobs: {e}")
        return []

def fetch_naukri_jobs():
    url = "https://www.naukri.com/python-jobs"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36'
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        jobs = []
        for i, job_card in enumerate(soup.select("article.jobTuple")):
            job = {
                "title": job_card.select_one("a.title").get_text(strip=True) if job_card.select_one("a.title") else "",
                "company": job_card.select_one("a.subTitle").get_text(strip=True) if job_card.select_one("a.subTitle") else "",
                "location": job_card.select_one(".loc span").get_text(strip=True) if job_card.select_one(".loc span") else "",
                "date": "N/A",
                "url": job_card.select_one("a.title")['href'] if job_card.select_one("a.title") else ""
            }
            jobs.append(job)
            if i == 4: break

        return jobs
    except Exception as e:
        logging.error(f"Failed to fetch Naukri jobs: {e}")
        return []

def fetch_company_jobs():
    return [
        {
            "title": "Backend Engineer",
            "company": "StartupOne",
            "location": "Remote",
            "date": "2025-06-25",
            "url": "https://startupone.com/careers/backend"
        },
        {
            "title": "Data Analyst",
            "company": "AnalyticsHub",
            "location": "Bangalore",
            "date": "2025-06-24",
            "url": "https://analyticshub.com/jobs/data-analyst"
        },
        # ...more static entries...
    ] * 5  # simulate 10 entries

def fetch_all():
    all_jobs = []

    logging.info("Fetching LinkedIn jobs...")
    all_jobs.extend(fetch_linkedin_jobs())
    time.sleep(random.uniform(1, 3))

    logging.info("Fetching Naukri jobs...")
    all_jobs.extend(fetch_naukri_jobs())
    time.sleep(random.uniform(1, 3))

    logging.info("Fetching Company Page jobs...")
    all_jobs.extend(fetch_company_jobs())

    # Deduplication
    unique_jobs = list({job['url']: job for job in all_jobs if job.get("url")}.values())

    with open("public/jobs.json", "w") as f:
        json.dump(unique_jobs, f, indent=2)

    logging.info(f"✅ Saved {len(unique_jobs)} unique jobs to public/jobs.json")

if __name__ == "__main__":
    fetch_all()
