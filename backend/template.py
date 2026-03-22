SUBJECT_TEMPLATE = "Internship Application — {role} at {company}"

BODY_TEMPLATE = """Hi {greeting},

I just submitted my application for the {role} position at {company} and wanted to reach out directly.

I'm a sophomore at the University of Illinois Urbana-Champaign studying Statistics and Computer Science with a Data Science minor. I have experience in machine learning research, full-stack development, and data engineering — and I'm genuinely excited about the work {company} is doing.

I'd love to connect or answer any questions you might have.

Best,
{your_name}
{your_email}
LinkedIn: {your_linkedin}
GitHub: {your_github}
"""

def format_email(
    recruiter_name: str | None,
    company: str,
    role: str,
    your_name: str,
    your_email: str,
    your_linkedin: str,
    your_github: str,
) -> dict:
    greeting = recruiter_name if recruiter_name else "Hiring Team"
    return {
        "subject": SUBJECT_TEMPLATE.format(role=role, company=company),
        "body": BODY_TEMPLATE.format(
            greeting=greeting,
            role=role,
            company=company,
            your_name=your_name,
            your_email=your_email,
            your_linkedin=your_linkedin,
            your_github=your_github,
        ),
    }
