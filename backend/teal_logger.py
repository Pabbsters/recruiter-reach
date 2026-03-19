import json
import os
import logging
import requests
from datetime import datetime
from backend import config

JOBS_FILE = os.path.join(os.path.dirname(__file__), "../jobs.json")
logger = logging.getLogger(__name__)

def _log_local(company: str, role: str, url: str, recruiter_email: str | None):
    jobs = []
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE) as f:
            jobs = json.load(f)
    jobs.append({
        "company": company,
        "role": role,
        "url": url,
        "recruiter_email": recruiter_email,
        "applied_at": datetime.now().isoformat(),
        "status": "Applied",
    })
    with open(JOBS_FILE, "w") as f:
        json.dump(jobs, f, indent=2)

def _log_teal(company: str, role: str, url: str):
    try:
        requests.post(
            "https://api.tealhq.com/v1/job_applications",
            headers={"Authorization": f"Bearer {config.TEAL_API_KEY}"},
            json={"company": company, "job_title": role, "job_url": url, "status": "applied"},
            timeout=5,
        )
    except Exception as e:
        logger.warning(f"Teal log failed (non-critical): {e}")

def log_job(company: str, role: str, url: str, recruiter_email: str | None):
    _log_local(company, role, url, recruiter_email)
    if config.TEAL_API_KEY:
        _log_teal(company, role, url)
