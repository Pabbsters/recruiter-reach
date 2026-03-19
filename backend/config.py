import os
from dotenv import load_dotenv

load_dotenv()

GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
GMAIL_REFRESH_TOKEN = os.getenv("GMAIL_REFRESH_TOKEN")
YOUR_NAME = os.getenv("YOUR_NAME", "Your Name")
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
YOUR_LINKEDIN = os.getenv("YOUR_LINKEDIN", "")
YOUR_GITHUB = os.getenv("YOUR_GITHUB", "")
TEAL_API_KEY = os.getenv("TEAL_API_KEY", "")

def validate():
    missing = [k for k, v in {
        "GMAIL_CLIENT_ID": GMAIL_CLIENT_ID,
        "GMAIL_CLIENT_SECRET": GMAIL_CLIENT_SECRET,
        "GMAIL_REFRESH_TOKEN": GMAIL_REFRESH_TOKEN,
        "YOUR_EMAIL": YOUR_EMAIL,
    }.items() if not v]
    if missing:
        raise RuntimeError(f"Missing required env vars: {missing}")
