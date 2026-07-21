import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

def send_alert(subject, body):
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    recipient = os.getenv("RECIPIENT_EMAIL")
    server_address = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", 587))
    if not all([user, password, recipient]):
        print("Missing email credentials in environment variables.")
        return
    msg = EmailMessage()
    msg['subject'] = subject
    msg.set_content(body)
    msg['to'] = recipient
    msg['from'] = user
    try:
        server = smtplib.SMTP(server_address, port)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
        server.quit()
        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")