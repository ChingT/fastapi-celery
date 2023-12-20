import os

from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()


class Config:
    CELERY_BROKER_URL: str = os.environ.get(
        "CELERY_BROKER_URL", "redis://localhost:6379"
    )
    CELERY_RESULT_BACKEND: str = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379"
    )
    CELERY_TASK_ROUTES = {
        "worker.*": {"queue": "high_priority"},
        "low_priority_tasks.*": {"queue": "low_priority"},
    }

    CELERY_BEAT_SCHEDULE: dict = {
        "send_credit_report": {
            "task": "credit_report",
            "schedule": crontab(),
            "options": {"queue": "periodic"},
        },
    }


settings = Config()
