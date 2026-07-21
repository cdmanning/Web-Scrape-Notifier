import os
import unittest
from message import send_alert
from unittest.mock import patch

class TestMessage(unittest.TestCase):

    @patch.dict(os.environ, {
        "SMTP_USER": "test_user@gmail.com",
        "SMTP_PASSWORD": "test_password",
        "SMTP_SERVER": "smtp.gmail.com",
        "SMTP_PORT": "587",
        "RECIPIENT_EMAIL": "alert@domain.com"
    })
    
    @patch('message.smtplib.SMTP')
    def test_send_alert_success(self, mock_smtp_class):
        mock_server_instance = mock_smtp_class.return_value
        send_alert("Test Subject", "Test Body")
        mock_smtp_class.assert_called_with("smtp.gmail.com", 587)
        mock_server_instance.starttls.assert_called_once()
        mock_server_instance.login.assert_called_with("test_user@gmail.com", "test_password")
        mock_server_instance.send_message.assert_called_once()
        mock_server_instance.quit.assert_called_once()

    @patch.dict(os.environ, clear=True)
    @patch('message.smtplib.SMTP')
    def test_send_alert_missing_credentials(self, mock_smtp_class):
        send_alert("Test Subject", "Test Body")
        mock_smtp_class.assert_not_called()

    @patch.dict(os.environ, {
        "SMTP_USER": "test_user",
        "SMTP_PASSWORD": "test_password",
        "RECIPIENT_EMAIL": "alert@domain.com"
    })
    
    @patch('message.smtplib.SMTP')
    def test_send_alert_smtp_exception(self, mock_smtp_class):
        mock_server_instance = mock_smtp_class.return_value
        mock_server_instance.login.side_effect = Exception("Auth Failed")
        send_alert("Test Subject", "Test Body")
        mock_server_instance.login.assert_called_once()

if __name__ == '__main__':
    unittest.main()