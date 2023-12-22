import os

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()


class Config:
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL")
    result_backend: str = os.environ.get("CELERY_RESULT_BACKEND")

    CELERY_BEAT_SCHEDULE: dict = {
        "send_credit_report": {
            "task": "credit_report",
            "schedule": crontab(),
            "options": {"queue": "periodic"},
        },
    }


settings = Config()


def create_celery():
    celery_app = Celery()
    celery_app.config_from_object(settings, namespace="CELERY")
    return celery_app
