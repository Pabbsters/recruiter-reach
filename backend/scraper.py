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
    # Naive slug: lowercase + strip non-alphanum + append .com
    clean = re.sub(r"[^a-z0-9]", "", company.lower().strip())
    return f"{clean}.com"

def _check_enrichlayer_credits() -> int:
    """Returns remaining credits. Returns 0 on error."""
    try:
        resp = requests.get(
            "https://nubela.co/proxycurl/api/credit-balance",
            headers={"Authorization": f"Bearer {config.ENRICHLAYER_API_KEY}"},
            timeout=5,
        )
        return resp.json().get("credit_balance", 0)
    except Exception:
        return 0

def _search_enrichlayer(company: str) -> dict | None:
    """Use EnrichLayer (ProxyCurl) person search to find a recruiter at the company."""
    if not config.ENRICHLAYER_API_KEY:
        return None
    credits = _check_enrichlayer_credits()
    if credits <= 0:
        logger.warning("EnrichLayer: no credits remaining — skipping, using fallback")
        return None
    logger.info(f"EnrichLayer: {credits} credits remaining")
    try:
        resp = requests.get(
            "https://nubela.co/proxycurl/api/search/person",
            params={
                "current_company_name": company,
                "headline": "recruiter",
                "page_size": 1,
            },
            headers={"Authorization": f"Bearer {config.ENRICHLAYER_API_KEY}"},
            timeout=10,
        )
        data = resp.json()
        results = data.get("results", [])
        if results:
            person = results[0].get("profile", {})
            first = person.get("first_name", "")
            last = person.get("last_name", "")
            if first and last:
                return {
                    "name": f"{first} {last}",
                    "domain": extract_domain(company),
                }
    except Exception as e:
        logger.warning(f"EnrichLayer search failed: {e}")
    return None

def _search_google_fallback(company: str) -> dict | None:
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
        logger.warning(f"Google fallback scrape failed: {e}")
    return None

def scrape_recruiter(company: str, role: str) -> dict:
    # Try EnrichLayer first (accurate), fall back to Google scrape
    result = _search_enrichlayer(company) or _search_google_fallback(company)
    if result:
        return result
    return {"name": None, "domain": extract_domain(company)}
