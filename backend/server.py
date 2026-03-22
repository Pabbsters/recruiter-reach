from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from backend.config import validate
from backend.scraper import scrape_recruiter
from backend.email_finder import generate_candidates
from backend.verifier import find_best
from backend.template import format_email
from backend.gmail_sender import send_email
from backend.teal_logger import log_job
from backend import config

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app, origins=["chrome-extension://*"])

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

    candidates = []
    verified_email = None

    if name:
        parts = name.split()
        if len(parts) >= 2:
            candidates = generate_candidates(parts[0], parts[1], domain)
            verified_email = find_best(candidates)

    if not verified_email:
        verified_email = find_best([f"recruiting@{domain}", f"careers@{domain}", f"talent@{domain}"])

    log_job(company, role, url, verified_email)

    if not verified_email:
        return jsonify({
            "success": False,
            "email_sent_to": None,
            "recruiter_name": name,
            "candidates_tried": len(candidates),
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
        "candidates_tried": len(candidates),
    })

if __name__ == "__main__":
    validate()
    app.run(port=5050, debug=False)
