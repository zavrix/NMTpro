import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import GMAIL_USER, GMAIL_PASSWORD

def send_email(subject, content, to, html=False):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = to

    if html:
        mime_text = MIMEText(content, "html")
    else:
        mime_text = MIMEText(content, "plain")

    msg.attach(mime_text)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, to, msg.as_string())
