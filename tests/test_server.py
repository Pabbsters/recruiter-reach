import pytest
from unittest.mock import patch

@pytest.fixture
def client():
    from backend.server import app
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

def test_reach_missing_fields(client):
    res = client.post("/reach", json={})
    assert res.status_code == 400
    assert "error" in res.get_json()

def test_reach_success(client):
    with patch("backend.server.scrape_recruiter", return_value={"name": "Jane Doe", "domain": "company.com"}), \
         patch("backend.server.generate_candidates", return_value=["jane.doe@company.com"]), \
         patch("backend.server.find_best", return_value="jane.doe@company.com"), \
         patch("backend.server.format_email", return_value={"subject": "s", "body": "b"}), \
         patch("backend.server.send_email", return_value=True), \
         patch("backend.server.log_job"):
        res = client.post("/reach", json={"company": "Company", "role": "Intern", "url": "https://x.com"})
        data = res.get_json()
        assert data["success"] is True
        assert data["email_sent_to"] == "jane.doe@company.com"

def test_reach_fallback_when_no_recruiter(client):
    with patch("backend.server.scrape_recruiter", return_value={"name": None, "domain": "company.com"}), \
         patch("backend.server.get_hunter_domain_info", return_value={}), \
         patch("backend.server.find_best", return_value=None), \
         patch("backend.server.log_job"):
        res = client.post("/reach", json={"company": "Company", "role": "Intern", "url": "https://x.com"})
        data = res.get_json()
        assert data["success"] is False
        assert data["email_sent_to"] is None
