import smtplib
import dns.resolver
import logging
import requests
from backend import config

logger = logging.getLogger(__name__)

def get_mx_record(domain: str) -> str | None:
    try:
        records = dns.resolver.resolve(domain, "MX")
        return str(sorted(records, key=lambda r: r.preference)[0].exchange)
    except Exception:
        return None

def verify_via_smtp(email: str) -> bool:
    """SMTP ping verification — blocked by many corporate servers."""
    domain = email.split("@")[1]
    mx = get_mx_record(domain)
    if not mx:
        return False
    try:
        with smtplib.SMTP(timeout=10) as smtp:
            smtp.connect(mx, 25)
            smtp.helo("check.local")
            smtp.mail("verify@check.local")
            code, _ = smtp.rcpt(email)
            return code == 250
    except Exception as e:
        logger.debug(f"SMTP check failed for {email}: {e}")
        return False

def verify_via_hunter(email: str) -> bool:
    """Hunter.io email verification — more reliable than SMTP."""
    if not config.HUNTER_API_KEY:
        return False
    try:
        resp = requests.get(
            "https://api.hunter.io/v2/email-verifier",
            params={"email": email, "api_key": config.HUNTER_API_KEY},
            timeout=10,
        )
        data = resp.json().get("data", {})
        status = data.get("status")
        # "valid" = confirmed exists, "accept_all" = server accepts all (still send)
        return status in ("valid", "accept_all")
    except Exception as e:
        logger.debug(f"Hunter verification failed for {email}: {e}")
        return False

def verify_email(email: str) -> bool:
    """Try Hunter first, fall back to SMTP."""
    if verify_via_hunter(email):
        return True
    return verify_via_smtp(email)

def find_best(candidates: list[str]) -> str | None:
    for email in candidates:
        if verify_email(email):
            logger.info(f"Verified email: {email}")
            return email
    return None
