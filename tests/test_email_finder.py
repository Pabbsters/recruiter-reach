from backend.email_finder import generate_candidates

def test_generates_common_patterns():
    candidates = generate_candidates("Jane", "Doe", "company.com")
    assert "jane.doe@company.com" in candidates
    assert "jdoe@company.com" in candidates
    assert "jane@company.com" in candidates
    assert "j.doe@company.com" in candidates

def test_all_lowercase():
    candidates = generate_candidates("JANE", "DOE", "Company.com")
    for email in candidates:
        assert email == email.lower()

def test_returns_list():
    result = generate_candidates("a", "b", "c.com")
    assert isinstance(result, list)
    assert len(result) > 0
