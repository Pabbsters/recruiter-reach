#!/bin/bash
set -e
echo "Setting up recruiter-reach..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env
echo "Done. Edit .env with your credentials then run ./start.sh"
