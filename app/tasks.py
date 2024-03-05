import time

from celery import Celery, shared_task
from fastapi.responses import JSONResponse

from app.broker_test import test_celery_broker_url
from app.settings import celery_backend_url, celery_broker_url

try:
    test_celery_broker_url()
    celery = Celery(__name__, broker=celery_broker_url, backend=celery_backend_url)
except Exception as e:
    raise e


@celery.task(name="push_notification")
def push_notification(input_token: str):
    time.sleep(5)
    return {"result": f"Notification sent to {input_token}"}
