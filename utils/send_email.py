import smtplib
from email.mime.text import MIMEText
from core.config import settings


def send_email_sync(to_email: str, subject: str, body: str):
    """
    :param to_email:
    :param subject:
    :param body:
    :return:
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(msg)
