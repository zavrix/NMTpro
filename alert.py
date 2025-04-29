# alert.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import GMAIL_USER, GMAIL_PASSWORD

def send_email(subject, content, to, html=False):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = GMAIL_USER
        msg["To"] = to

        mime_type = "html" if html else "plain"
        mime_text = MIMEText(content, mime_type)
        msg.attach(mime_text)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, to, msg.as_string())

    except Exception as e:
        print(f"[ERROR] Email sending failed: {e}")
