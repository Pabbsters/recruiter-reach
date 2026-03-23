import re
import logging
import requests
from bs4 import BeautifulSoup
from backend import config

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def extract_domain(company: str) -> str:
    clean = re.sub(r"[^a-z0-9]", "", company.lower().strip())
    return f"{clean}.com"

def get_hunter_domain_info(domain: str) -> dict:
    """
    Uses Hunter.io domain search to get:
    - email pattern (e.g. {first}.{last}@company.com)
    - list of known verified emails at the domain
    Returns empty dict if Hunter key not set or call fails.
    """
    if not config.HUNTER_API_KEY:
        return {}
    try:
        resp = requests.get(
            "https://api.hunter.io/v2/domain-search",
            params={"domain": domain, "api_key": config.HUNTER_API_KEY, "limit": 5},
            timeout=10,
        )
        data = resp.json().get("data", {})
        return {
            "pattern": data.get("pattern"),          # e.g. "{first}.{last}"
            "emails": [e["value"] for e in data.get("emails", []) if e.get("value")],
        }
    except Exception as e:
        logger.warning(f"Hunter domain search failed: {e}")
    return {}

def find_email_via_hunter(first: str, last: str, domain: str) -> str | None:
    """Uses Hunter.io email finder to get the most likely email for a specific person."""
    if not config.HUNTER_API_KEY:
        return None
    try:
        resp = requests.get(
            "https://api.hunter.io/v2/email-finder",
            params={
                "domain": domain,
                "first_name": first,
                "last_name": last,
                "api_key": config.HUNTER_API_KEY,
            },
            timeout=10,
        )
        data = resp.json().get("data", {})
        email = data.get("email")
        score = data.get("score", 0)
        if email and score >= 50:
            return email
    except Exception as e:
        logger.warning(f"Hunter email finder failed: {e}")
    return None

def _search_google_for_recruiter(company: str) -> dict | None:
    """Fallback: Google search for LinkedIn recruiter profiles."""
    query = f'site:linkedin.com/in recruiter OR "talent acquisition" "{company}"'
    try:
        resp = requests.get(
            "https://www.google.com/search",
            params={"q": query},
            headers=HEADERS,
            timeout=10,
        )
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup.find_all("h3"):
            text = tag.get_text()
            if any(w in text.lower() for w in ["recruit", "talent", "hr", "people"]):
                name_match = re.match(r"^([A-Z][a-z]+ [A-Z][a-z]+)", text)
                if name_match:
                    return {
                        "name": name_match.group(1),
                        "domain": extract_domain(company),
                    }
    except Exception as e:
        logger.warning(f"Google scrape failed: {e}")
    return None

def scrape_recruiter(company: str, role: str) -> dict:
    domain = extract_domain(company)
    result = _search_google_for_recruiter(company)
    name = result.get("name") if result else None
    return {"name": name, "domain": domain}
