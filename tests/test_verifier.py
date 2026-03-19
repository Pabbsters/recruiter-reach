from unittest.mock import patch, MagicMock
from backend.verifier import verify_email, find_best

def test_returns_bool():
    with patch("backend.verifier.smtplib.SMTP") as mock_smtp:
        mock_conn = MagicMock()
        mock_smtp.return_value.__enter__ = lambda s: mock_conn
        mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.rcpt.return_value = (250, b"OK")
        with patch("backend.verifier.get_mx_record", return_value="mx.example.com"):
            result = verify_email("test@example.com")
            assert isinstance(result, bool)

def test_invalid_domain_returns_false():
    result = verify_email("test@thisdoesnotexist12345xyz.com")
    assert result is False

def test_find_best_returns_first_valid():
    with patch("backend.verifier.verify_email", side_effect=[False, True, False]):
        result = find_best(["a@x.com", "b@x.com", "c@x.com"])
        assert result == "b@x.com"

def test_find_best_returns_none_when_all_invalid():
    with patch("backend.verifier.verify_email", return_value=False):
        result = find_best(["a@x.com", "b@x.com"])
        assert result is None
