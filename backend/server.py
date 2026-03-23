from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from backend.config import validate
from backend.scraper import scrape_recruiter, get_hunter_domain_info, find_email_via_hunter
from backend.email_finder import generate_candidates
from backend.verifier import find_best
from backend.template import format_email
from backend.gmail_sender import send_email
from backend.teal_logger import log_job
from backend import config

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app, origins=["chrome-extension://*"])

# Common recruiting inbox patterns — tried in order when no specific recruiter found
RECRUITING_PATTERNS = [
    "recruiting", "recruiter", "careers", "talent", "hr",
    "hiring", "jobs", "apply", "people", "humanresources",
]

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/reach", methods=["POST"])
def reach():
    data = request.get_json()
    company = (data.get("company") or "").strip()
    role = (data.get("role") or "").strip()
    url = (data.get("url") or "").strip()

    if not company or not role:
        return jsonify({"success": False, "error": "company and role required"}), 400

    recruiter = scrape_recruiter(company, role)
    name = recruiter.get("name")
    domain = recruiter.get("domain")

    verified_email = None
    candidates_tried = []

    # Step 1: If we have a recruiter name, use Hunter to find their specific email
    if name:
        parts = name.split()
        if len(parts) >= 2:
            hunter_email = find_email_via_hunter(parts[0], parts[1], domain)
            if hunter_email:
                candidates_tried.append(hunter_email)
                from backend.verifier import verify_email
                if verify_email(hunter_email):
                    verified_email = hunter_email

    # Step 2: Use Hunter domain search to get known emails + pattern-based candidates
    if not verified_email:
        hunter_info = get_hunter_domain_info(domain)

        # Try known emails from Hunter first (highest confidence)
        known_emails = hunter_info.get("emails", [])
        candidates_tried.extend(known_emails)
        if known_emails:
            verified_email = find_best(known_emails)

    # Step 3: If Hunter gave us a pattern, generate pattern-based candidates for recruiter name
    if not verified_email and name:
        parts = name.split()
        if len(parts) >= 2:
            pattern_candidates = generate_candidates(parts[0], parts[1], domain)
            candidates_tried.extend(pattern_candidates)
            verified_email = find_best(pattern_candidates)

    # Step 4: Try all common recruiting inbox patterns
    if not verified_email:
        recruiting_emails = [f"{p}@{domain}" for p in RECRUITING_PATTERNS]
        candidates_tried.extend(recruiting_emails)
        verified_email = find_best(recruiting_emails)

    # Log the job regardless of whether we found an email
    log_job(company, role, url, verified_email)

    if not verified_email:
        return jsonify({
            "success": False,
            "email_sent_to": None,
            "recruiter_name": name,
            "candidates_tried": len(candidates_tried),
            "error": "No verified email found — job logged, no email sent.",
        })

    email_content = format_email(
        recruiter_name=name,
        company=company,
        role=role,
        your_name=config.YOUR_NAME,
        your_email=config.YOUR_EMAIL,
        your_linkedin=config.YOUR_LINKEDIN,
        your_github=config.YOUR_GITHUB,
    )

    sent = send_email(verified_email, email_content["subject"], email_content["body"])

    return jsonify({
        "success": sent,
        "recruiter_name": name,
        "email_sent_to": verified_email,
        "candidates_tried": len(candidates_tried),
    })

if __name__ == "__main__":
    validate()
    app.run(port=5050, debug=False)
