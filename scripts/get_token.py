"""
Run this once to get your Gmail refresh token, then paste values into .env

Usage:
    python scripts/get_token.py credentials.json
"""
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

if len(sys.argv) < 2:
    print("Usage: python scripts/get_token.py credentials.json")
    sys.exit(1)

flow = InstalledAppFlow.from_client_secrets_file(
    sys.argv[1],
    scopes=["https://www.googleapis.com/auth/gmail.send"]
)
creds = flow.run_local_server(port=0)
print("\n--- Copy these into your .env ---")
print(f"GMAIL_CLIENT_ID={creds.client_id}")
print(f"GMAIL_CLIENT_SECRET={creds.client_secret}")
print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")
