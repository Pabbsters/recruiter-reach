# recruiter-reach

> Find the recruiter's verified email on any job posting and send a personalized outreach — in one click.

A Chrome extension + local Python backend that:
1. Reads the company name and job title from any job posting
2. Scrapes LinkedIn public search to find the recruiter's name
3. Generates email pattern candidates and SMTP-verifies the real one
4. Sends a personalized email via your Gmail
5. Logs the job to Teal and a local `jobs.json`

**100% free. Runs locally. Nothing leaves your machine.**

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/Pabbsters/recruiter-reach.git
cd recruiter-reach
./setup.sh
```

### 2. Configure Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → Enable **Gmail API**
3. Create **OAuth 2.0 credentials** (Desktop app) → Download `credentials.json`
4. Run once to get your refresh token:

```bash
source .venv/bin/activate
python scripts/get_token.py credentials.json
```

5. Fill in `.env` with the printed values (see `.env.example` for all fields)

### 3. Start the backend

```bash
./start.sh
```

**Auto-start on Mac login (optional — never think about it again):**

```bash
cp com.recruiterreach.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.recruiterreach.plist
```

### 4. Load the Chrome extension

1. Open Chrome → `chrome://extensions`
2. Enable **Developer mode** (top right)
3. Click **Load unpacked** → select the `extension/` folder

---

## Usage

1. Navigate to any job posting (LinkedIn, Workday, Greenhouse, etc.)
2. Click the **recruiter-reach** icon in your Chrome toolbar
3. Verify the detected company + role
4. Click **Send Outreach**

Done — email sent, job logged to `jobs.json`.

---

## How it works

| Step | What happens |
|------|-------------|
| 1 | Extension reads company + job title from the page |
| 2 | Backend searches Google for LinkedIn recruiter profiles at the company |
| 3 | Generates 11 email pattern candidates |
| 4 | SMTP-verifies each candidate against the mail server |
| 5 | Sends personalized email via Gmail API |
| 6 | Logs to `jobs.json` + Teal (if API key set) |

**Accuracy:** ~50-70% verified hit rate. Falls back to `recruiting@company.com` when no verified match found.

---

## Customizing your email template

Edit `backend/template.py` — change `BODY_TEMPLATE` to match your voice. Variables available: `{greeting}`, `{role}`, `{company}`, `{your_name}`, `{your_email}`, `{your_linkedin}`, `{your_github}`.

---

## Tech Stack

- **Python 3.13+** — Flask, BeautifulSoup4, google-api-python-client, dnspython
- **JavaScript** — Chrome Extension (Manifest V3)
- **Gmail API** — OAuth 2.0 for sending

## Running tests

```bash
source .venv/bin/activate
pytest tests/ -v
```

## Contributing

PRs welcome. Open an issue first for major changes.

## License

MIT
