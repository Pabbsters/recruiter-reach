import json
import os
import tempfile
from unittest.mock import patch
from backend.teal_logger import log_job, _log_local

def test_log_local_creates_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        jobs_path = os.path.join(tmpdir, "jobs.json")
        with patch("backend.teal_logger.JOBS_FILE", jobs_path):
            _log_local("Nasdaq", "Data Science Intern", "https://example.com", "recruiter@nasdaq.com")
            assert os.path.exists(jobs_path)
            with open(jobs_path) as f:
                jobs = json.load(f)
            assert len(jobs) == 1
            assert jobs[0]["company"] == "Nasdaq"

def test_log_local_appends():
    with tempfile.TemporaryDirectory() as tmpdir:
        jobs_path = os.path.join(tmpdir, "jobs.json")
        with patch("backend.teal_logger.JOBS_FILE", jobs_path):
            _log_local("A", "Role1", "url1", None)
            _log_local("B", "Role2", "url2", None)
            with open(jobs_path) as f:
                jobs = json.load(f)
            assert len(jobs) == 2

def test_log_job_skips_teal_when_no_key():
    with patch("backend.teal_logger._log_local") as mock_local, \
         patch("backend.teal_logger._log_teal") as mock_teal, \
         patch("backend.teal_logger.config") as mock_config:
        mock_config.TEAL_API_KEY = ""
        log_job("Nasdaq", "Intern", "url", "email@x.com")
        mock_local.assert_called_once()
        mock_teal.assert_not_called()
