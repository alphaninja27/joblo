
# 🧠 Joblo - Smart Job Matcher

Joblo is an intelligent job-matching platform that scrapes jobs from multiple sources, embeds them semantically, and ranks results based on natural-language queries.

---

## 🚀 Live URLs

- **Frontend (Vercel):** https://joblo.vercel.app  
- **Backend API (Render):** https://joblo-1bvy.onrender.com/api/match  

---

## 📦 Project Structure

```

joblo/
├── backend/                # FastAPI + FAISS backend
│   ├── app.py              # Main API server
│   ├── fetch\_jobs.py       # Scraper for LinkedIn, Naukri, etc.
│   ├── generate\_vectors.py # Embedding generator for jobs
│   ├── public/             # Stores jobs.json & job\_vectors.json
│   └── requirements.txt
├── frontend/               # React + Vite frontend
│   └── .env                # VITE\_API\_URL=[https://joblo-1bvy.onrender.com](https://joblo-1bvy.onrender.com)
├── .github/workflows/ci.yml # GitHub Actions CI/CD
└── README.md

````

---

## ✅ Features

- 🔍 Natural-language job search (e.g. "remote python jobs in bangalore")
- 🤖 Semantic embeddings with `sentence-transformers`
- ⚡ Vector-based search via FAISS
- 🌐 Full-stack deployment with Vercel (FE) & Render (BE)
- 🛠 GitHub Actions CI/CD

---

## 🛠 Local Setup

### 1. Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python fetch_jobs.py           # Fetch job listings
python generate_vectors.py     # Generate embeddings
uvicorn app:app --reload
````

`.env` (already set on Render):

```
COHERE_API_KEY=your-cohere-api-key
```

### 2. Frontend

```bash
cd frontend
npm install
```

`.env`:

```
VITE_API_URL=https://joblo-1bvy.onrender.com
```

```bash
npm run dev
```

---

## 🧪 Testing & Monitoring

* End-to-end test: scraper → matcher → UI flow
* Metrics: scrape success rate, query latency
* Alerts: console logs + Render dashboard
* CI/CD: GitHub Actions lints, tests, builds, and deploys

---

## 🧠 CLI Mode Example

```bash
python cli.py
🔍 Enter your job query: remote python jobs in bangalore

1. Backend Engineer at StartupOne (Remote)
   🔗 https://startupone.com/careers/backend
```

---

## 📤 Deployment

* Frontend auto-deployed on push to `main` via **Vercel**
* Backend auto-deployed on push to `master` via **Render**
* GitHub Actions handles test → build → deploy


