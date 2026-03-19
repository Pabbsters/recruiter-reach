from unittest.mock import patch, MagicMock

def test_send_email_returns_true_on_success():
    with patch("backend.gmail_sender._get_service") as mock_svc:
        mock_service = MagicMock()
        mock_svc.return_value = mock_service
        mock_service.users.return_value.messages.return_value.send.return_value.execute.return_value = {"id": "123"}
        from backend.gmail_sender import send_email
        result = send_email("recruiter@company.com", "Subject", "Body")
        assert result is True

def test_send_email_returns_false_on_exception():
    with patch("backend.gmail_sender._get_service") as mock_svc:
        mock_svc.side_effect = Exception("Auth failed")
        from backend.gmail_sender import send_email
        result = send_email("recruiter@company.com", "Subject", "Body")
        assert result is False
