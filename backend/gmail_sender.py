import base64
import logging
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from backend import config

logger = logging.getLogger(__name__)

def _get_service():
    creds = Credentials(
        token=None,
        refresh_token=config.GMAIL_REFRESH_TOKEN,
        client_id=config.GMAIL_CLIENT_ID,
        client_secret=config.GMAIL_CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token",
    )
    return build("gmail", "v1", credentials=creds)

def send_email(to: str, subject: str, body: str) -> bool:
    try:
        service = _get_service()
        message = MIMEText(body)
        message["to"] = to
        message["from"] = config.YOUR_EMAIL
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId="me", body={"raw": raw}).execute()
        return True
    except Exception as e:
        logger.error(f"Gmail send failed: {e}")
        return False
