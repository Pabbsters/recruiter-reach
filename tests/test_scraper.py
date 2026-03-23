# Note: extract_domain is a naive slug converter (lowercase + strip non-alphanum + .com)
# It is not an authoritative domain lookup — accuracy depends on company name simplicity.
from unittest.mock import patch
from backend.scraper import extract_domain, scrape_recruiter

def test_extract_domain_simple():
    assert extract_domain("Google") == "google.com"

def test_extract_domain_strips_spaces():
    assert extract_domain("  Nasdaq  ") == "nasdaq.com"

def test_extract_domain_multiword():
    assert extract_domain("Goldman Sachs") == "goldmansachs.com"

def test_scrape_recruiter_returns_dict():
    with patch("backend.scraper._search_google_for_recruiter", return_value={"name": "Jane Doe", "domain": "nasdaq.com"}):
        result = scrape_recruiter("Nasdaq", "Data Science Intern")
        assert "name" in result
        assert "domain" in result

def test_scrape_recruiter_falls_back_on_failure():
    with patch("backend.scraper._search_google_for_recruiter", return_value=None):
        result = scrape_recruiter("Nasdaq", "Data Science Intern")
        assert result["domain"] == "nasdaq.com"
        assert result["name"] is None
