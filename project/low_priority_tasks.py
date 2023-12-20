import time

from celery import shared_task


@shared_task
def generate_transaction_report(user_id=1):
    time.sleep(5)
    return True
