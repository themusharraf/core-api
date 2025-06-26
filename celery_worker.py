from celery import Celery
from celery.schedules import crontab
from core.config import settings

celery_app = Celery(
    "core_api",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

import tasks.email_tasks
import tasks.cleanup

celery_app.conf.task_routes = {
    "tasks.email_tasks.send_verification_email": {"queue": "email"},
    "tasks.cleanup.delete_old_unverified_users": {"queue": "cleanup"},
}

celery_app.conf.beat_schedule = {
    "delete-old-unverified-users-every-night": {
        "task": "tasks.cleanup.delete_old_unverified_users",
        "schedule": crontab(hour=3, minute=0),
        # "schedule": crontab(minute="*/1"),

    },
}
