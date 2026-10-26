# AI-Based Threat Intelligence Platform (AegisAI)

> **DEFENSIVE & EDUCATIONAL USE ONLY**  
> *College Case Study & Cybersecurity Capstone Benchmark Project*  
> This platform demonstrates automated cyber threat detection using explainable machine learning models. It is designed solely for defensive analysis and educational study. It does **not** contain or generate exploit code, attack tooling, malware, or weaponized payloads.

---

## 1. Project Overview

Modern Security Operations Centers (SOCs) are burdened by thousands of disjointed alerts, high false-positive rates, and slow signature updates. **AegisAI** is a full-stack automated threat intelligence and incident triage platform that provides:

1. **Phishing URL Detection (Explainable AI)**: Evaluates lexical features, Shannon entropy, and security keywords using **XGBoost** and **Random Forest**, reporting a confidence score and human-readable risk factors.
2. **Network Intrusion Detection**: Combines a supervised **Random Forest** classifier (for known DoS, Probe, and R2L attacks) with an unsupervised **Isolation Forest** (for zero-day and anomalous NetFlow detection) on NSL-KDD and UNSW-NB15 schemas.
3. **Login Anomaly Detection (UEBA)**: Uses an **Isolation Forest** trained on normal employee baselines to flag credential stuffing bursts, impossible geographic travel, and unauthorized off-hours access.
4. **Threat Intelligence Dashboard**: Displays real-time KPIs, temporal incident trends, threat type distributions, and active alert feeds.
5. **Model Registry & Auditing**: Dynamically computes and displays the exact number of datasets, records trained on, feature counts, and confusion matrices directly from `metadata.json` (zero hardcoded values).
6. **Continuous Retraining Feedback Loop**: Empowers SOC analysts to triage and review alerts. The "Retrain model" pipeline merges analyst-verified labels with original baseline datasets and recalibrates model weights and metrics.

---

## 2. Tech Stack

- **Backend**: Python 3.11, FastAPI, Pydantic v2, SQLAlchemy, SQLite, Uvicorn
- **Machine Learning**: Scikit-Learn 1.9+, XGBoost 3.2+, Pandas, NumPy, Joblib, Matplotlib
- **Frontend**: React 19, Vite, Tailwind CSS 3.4, Recharts, Lucide React, Axios
- **Database**: SQLite (`threat_intel.db`) for alert audit trails, scan records, and retraining logs

---

## 3. Directory Structure

```text
Ai Threat/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI entry point, CORS, routers & startup seed
│   │   ├── database.py            # SQLite engine & SessionLocal dependency
│   │   ├── models/                # SQLAlchemy ORM models (Alert, ScanRecord, RetrainLog)
│   │   ├── schemas/               # Pydantic v2 validation models (URL, Network, Login, Alert)
│   │   └── routers/
│   │       ├── predict.py         # /predict/url, /predict/network, /predict/login
│   │       ├── alerts.py          # /alerts, /alerts/{id}/review
│   │       ├── dashboard.py       # /dashboard/stats
│   │       ├── models_info.py     # /models/info (Dynamic metadata API)
│   │       └── retrain.py         # /retrain (Analyst feedback pipeline)
│   ├── data/
│   │   ├── raw/                   # Sample subsets (UCI Phishing, NSL-KDD, UNSW-NB15)
│   │   ├── processed/             # Cleaned splits & synthetic UEBA data
│   │   ├── generate_datasets.py   # Dataset builder & synthesizer
│   │   └── download_datasets.py   # Public academic datasets fetcher
│   ├── ml/
│   │   ├── features.py            # URL lexical & entropy feature extractor
│   │   ├── train_phishing.py      # Phishing pipeline (RF vs XGBoost)
│   │   ├── train_network.py       # Network intrusion pipeline (RF + Isolation Forest)
│   │   ├── train_login.py         # UEBA login anomaly pipeline (Isolation Forest)
│   │   ├── train_all.py           # Single-command unified training script
│   │   ├── evaluate.py            # Generates ROC curves & confusion matrix plots
│   │   └── metadata_manager.py    # Computes live metadata.json from real data
│   ├── models_saved/              # Serialized .joblib artifacts, plots, & metadata.json
│   └── tests/
│       ├── test_features.py       # Unit tests for URL feature extraction
│       └── test_api.py            # Unit & integration tests for all FastAPI endpoints
├── frontend/
│   ├── src/
│   │   ├── components/            # Sidebar, Navbar, StatCard, SeverityBadge, AlertReviewModal
│   │   ├── pages/                 # Home, Dashboard, PhishingScan, NetworkScan, LoginAnomaly, Alerts, ModelInfo
│   │   ├── services/api.js        # Axios API client
│   │   ├── App.jsx                # Layout & view routing
│   │   └── index.css              # Cyber-dark theme & glassmorphism styles
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── PROGRESS.md                    # Verification & task tracker
├── requirements.txt               # Backend dependencies
├── .env.example                   # Environment configuration template
└── README.md                      # Comprehensive project documentation
```

---

## 4. Setup & Installation

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- `uv` (recommended) or standard `python3 -m venv`

### Backend Setup
1. Open a terminal and navigate to the project root:
   ```bash
   cd "/Users/varadramchandrapatil/Desktop/Ai Threat"
   ```
2. Activate the virtual environment (created with Python 3.11):
   ```bash
   source .venv/bin/activate
   ```
   *(If creating a new virtual environment from scratch, run `uv venv .venv --python 3.11 && source .venv/bin/activate && uv pip install -r requirements.txt`)*
3. Ensure dependencies are up to date:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy environment configuration:
   ```bash
   cp .env.example .env
   ```

### Frontend Setup
1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install frontend dependencies:
   ```bash
   npm install
   ```

---

## 5. Dataset Information & Download Guide

The platform includes pre-bundled, ready-to-run sample datasets so that the application trains and functions **immediately out of the box** without requiring gigabytes of downloads:

1. **UCI Phishing Websites Dataset Sample** (`backend/data/raw/phishing_sample.csv`):
   - 1,200 labeled URL samples (600 legitimate, 600 phishing).
   - Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/327/phishing+websites).
2. **NSL-KDD Benchmarking Dataset Sample** (`backend/data/raw/nsl_kdd_sample_train.csv`, `nsl_kdd_sample_test.csv`):
   - 1,200 Train / 350 Test official split records across 36 preprocessed features.
   - Source: [Canadian Institute for Cybersecurity (CIC)](https://www.unb.ca/cic/datasets/nsl.html).
3. **UNSW-NB15 Modern Intrusion Dataset Sample** (`backend/data/raw/unsw_nb15_sample_train.csv`, `unsw_nb15_sample_test.csv`):
   - 1,200 Train / 350 Test official split records covering contemporary network attack categories.
   - Source: [UNSW Australian Centre for Cyber Security (ACCS)](https://research.unsw.edu.au/projects/unsw-nb15-dataset).
4. **Synthetic UEBA Login Profiles** (`backend/data/processed/ueba_logins_synthetic.csv`):
   - 1,950 total records (1,800 normal baseline sessions, 150 injected anomalies).
   - Clearly tagged as `[SYNTHETIC_DATASET_V1]`.

### Optional: Downloading Full Upstream Datasets
To fetch the full raw academic archives, execute:
```bash
python backend/data/download_datasets.py
```

---

## 6. How to Train the Machine Learning Models

### Train All Models with a Single Command
To train the Phishing, Network Intrusion, and UEBA models sequentially, compute dynamic performance metrics, and generate `metadata.json`:
```bash
python backend/ml/train_all.py
```

### Train Individual Modules
- **Phishing URL Detector**:
  ```bash
  python backend/ml/train_phishing.py
  ```
- **Network Intrusion Detector**:
  ```bash
  python backend/ml/train_network.py
  ```
- **UEBA Login Anomaly Detector**:
  ```bash
  python backend/ml/train_login.py
  ```

### Generate Evaluation Plots (Confusion Matrices & ROC Curves)
```bash
python backend/ml/evaluate.py
```
*Visual artifacts are saved to `backend/models_saved/plots/`.*

---

## 7. How to Run the Application

Run the application using two separate terminals:

### Terminal 1: Backend Server (FastAPI)
```bash
cd "/Users/varadramchandrapatil/Desktop/Ai Threat"
source .venv/bin/activate
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Base URL: `http://127.0.0.1:8000`
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc Documentation: `http://127.0.0.1:8000/redoc`

### Terminal 2: Frontend Client (Vite + React)
```bash
cd "/Users/varadramchandrapatil/Desktop/Ai Threat/frontend"
npm run dev
```
- Web Application UI: `http://localhost:5173`

---

## 8. Running Automated Unit & API Tests

Execute the automated test suite covering feature extraction, risk explainability, and all REST endpoints:
```bash
PYTHONPATH=. .venv/bin/pytest backend/tests/ -v
```
All 13 unit tests pass:
- `test_root_endpoint`
- `test_predict_url_safe`
- `test_predict_url_phishing`
- `test_predict_login_normal`
- `test_predict_login_anomaly`
- `test_predict_network_default_sample`
- `test_models_info`
- `test_alerts_and_review`
- `test_dashboard_stats`
- `test_retraining_endpoint`
- `test_legitimate_url_features`
- `test_phishing_url_features_detection`
- `test_entropy_calculation`

---

## 10. Deployment Architecture & Cloud Setup

AegisAI supports two primary deployment topologies:

### Layout (A): Unified Vercel Deployment (Recommended & Implemented)
Both the **Vite + React frontend** and the **FastAPI Python backend** run on Vercel under a shared domain using **Vercel Services**:
- **Bundle Size Optimization**: Dev dependencies (`pytest`, `httpx`, `matplotlib`, `seaborn`) are separated from production dependencies. The total uncompressed serverless bundle is ~250 MB, well under Vercel's **500 MB** function size limit.
- **Unified Routing**: Requests to `/api/*` and direct backend endpoints (`/predict/*`, `/alerts/*`, `/dashboard/*`, `/models/*`, `/retrain/*`, `/docs`) route to FastAPI. All other routes `/(.*)` route to the Vite SPA with full refresh support.
- **Serverless-Safe Storage**: SQLite automatically uses `/tmp/threat_intel.db` when running on Vercel (`VERCEL=1`), or PostgreSQL when `DATABASE_URL` is set.
- **4.5 MB Payload Protection**: Both the frontend file selector and the FastAPI `/predict/network` route validate and reject CSV uploads exceeding Vercel's 4.5 MB serverless payload limit with friendly HTTP 413 error messages.
- **Safe Model Retraining**: On serverless functions, retraining fails gracefully with a descriptive error informing users that retraining runs locally or on persistent containers.

#### Required Environment Variables for Vercel (Layout A)
| Variable | Value / Description | Required? |
|---|---|---|
| `DATABASE_URL` | Optional. If unset, automatically defaults to `sqlite:////tmp/threat_intel.db`. To persist across cold starts, supply a managed Postgres connection string (e.g. Neon, Supabase, Render). | Optional |
| `CORS_ORIGINS` | Optional. e.g. `https://your-app.vercel.app` (defaults to permissive in dev). | Optional |
| `ENVIRONMENT` | `production` | Optional |

#### Exact Deployment Steps for Vercel:
1. Push project code to GitHub/GitLab.
2. In the Vercel Dashboard, import the repository.
3. Vercel automatically detects `vercel.json` and creates two services: `app` (FastAPI at root `.`) and `frontend` (Vite in `frontend/`).
4. (Optional) Set `DATABASE_URL` if using external PostgreSQL.
5. Click **Deploy**.
6. Or deploy from CLI:
   ```bash
   npx vercel --prod
   ```

---

### Layout (B): Split Deployment (Vercel Frontend + Render Backend)
If you prefer persistent disk storage for SQLite or want in-cloud model retraining without serverless function limits:
1. **Deploy Backend to Render**:
   - Create a **Web Service** pointing to the repository.
   - Build Command: `pip install -r requirements.txt` (or `uv pip install -r requirements.txt`)
   - Start Command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - Set environment variable `CORS_ORIGINS=https://your-frontend.vercel.app`
2. **Deploy Frontend to Vercel**:
   - Set Root Directory: `frontend`
   - Set Environment Variable: `VITE_API_URL=https://your-backend.onrender.com`
   - Deploy.

---

## 11. Limitations & Data Provenance Disclosure

In compliance with academic case study guidelines:

1. **Synthetic vs. Real Data**:
   - **Real / Public Benchmarks**: Phishing URL features are derived from the public **UCI Phishing Websites** repository. Network intrusion features and protocol structures follow the official **NSL-KDD** and **UNSW-NB15** benchmarking schemas.
   - **Synthetic UEBA Telemetry**: Enterprise login histories, user profiles, and login anomalies are generated deterministically using a seeded random generator (Seed: 42) and are explicitly labeled in the database and UI with `[SYNTHETIC_DATASET_V1]`. This is done to protect privacy while accurately modeling UEBA behaviors (off-hours access, credential velocity, impossible travel).
2. **Defensive Scope**:
   - This platform performs **detection and classification only**. It does not perform active blocking, firewall rule execution, DNS redirection, or automated account lockouts.
3. **Machine Learning Generalization**:
   - Machine learning models can produce false positives and false negatives. Model outputs should serve as decision-support telemetry for human analysts rather than autonomous production actions.

---

## 12. Educational Disclaimer

> **DISCLAIMER:**  
> This software is created strictly for academic research, education, and college case study presentations. It is intended to showcase automated detection methodologies and explainable AI in defensive cybersecurity. Do not deploy this software as the sole security control in a production environment.

