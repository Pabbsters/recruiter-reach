import smtplib
import dns.resolver
import logging

logger = logging.getLogger(__name__)

def get_mx_record(domain: str) -> str | None:
    try:
        records = dns.resolver.resolve(domain, "MX")
        return str(sorted(records, key=lambda r: r.preference)[0].exchange)
    except Exception:
        return None

def verify_email(email: str) -> bool:
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

def find_best(candidates: list[str]) -> str | None:
    for email in candidates:
        if verify_email(email):
            return email
    return None
