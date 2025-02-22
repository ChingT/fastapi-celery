import random
import time

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger("tasks")


@shared_task
def create_task(task_type):
    time.sleep(int(task_type) * 2)
    return True


@shared_task
def push_error_task(device_token: str):
    logger.info("starting background task")
    time.sleep(2)
    11 / 0
    logger.info(f"notification sent {device_token}")


@shared_task(bind=True)
def send_notification(self, device_token: str):
    try:
        logger.info("starting background task")
        time.sleep(1)
        if random.choice([0, 1]):
            raise Exception()
    except Exception as e:
        raise self.retry(exc=e, countdown=3, max_retries=3)
    logger.info(f"notification sent {device_token}")


@shared_task(name="credit_report")
def send_credit_analysis():
    logger.info("Generated and sent credit analysis to all active users")
    return True
