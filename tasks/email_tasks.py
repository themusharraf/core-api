from celery_worker import celery_app
from utils.send_email import send_email_sync


@celery_app.task(name="tasks.email_tasks.send_verification_email")
def send_verification_email(email: str, code: str):
    """
    :param email:
    :param code:
    :return:
    """
    subject = "Your verification code"
    body = f"Your verification code is: {code}"
    send_email_sync(email, subject, body)
