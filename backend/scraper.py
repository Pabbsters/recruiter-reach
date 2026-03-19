import re
import logging
import requests
from bs4 import BeautifulSoup

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
    # Works well for single-word companies; multi-word loses spaces
    clean = re.sub(r"[^a-z0-9]", "", company.lower().strip())
    return f"{clean}.com"

def _search_linkedin(company: str, role: str) -> dict | None:
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
        logger.warning(f"LinkedIn scrape failed: {e}")
    return None

def scrape_recruiter(company: str, role: str) -> dict:
    result = _search_linkedin(company, role)
    if result:
        return result
    return {"name": None, "domain": extract_domain(company)}
