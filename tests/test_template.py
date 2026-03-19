from backend.template import format_email

def test_fills_all_fields():
    result = format_email(
        recruiter_name="Jane",
        company="Nasdaq",
        role="Data Science Intern",
        your_name="Ruthwik Pabbu",
        your_email="rpabbu2@illinois.edu",
        your_linkedin="https://linkedin.com/in/ruthwikpabbu",
        your_github="https://github.com/Pabbsters"
    )
    assert "Jane" in result["body"]
    assert "Nasdaq" in result["body"]
    assert "Data Science Intern" in result["body"]
    assert "Ruthwik" in result["body"]
    assert "subject" in result
    assert "body" in result

def test_falls_back_when_no_name():
    result = format_email(
        recruiter_name=None,
        company="Nasdaq",
        role="Data Science Intern",
        your_name="Ruthwik Pabbu",
        your_email="rpabbu2@illinois.edu",
        your_linkedin="",
        your_github=""
    )
    assert "Hiring Team" in result["body"]
