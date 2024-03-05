import logging
import time

from celery import Celery, shared_task
from celery.signals import after_setup_logger
from celery.utils.log import get_task_logger
from fastapi.responses import JSONResponse

from app.broker_test import test_celery_broker_url
from app.settings import celery_backend_url, celery_broker_url

logger = get_task_logger("tasks")

try:
    test_celery_broker_url()
    celery = Celery(__name__, broker=celery_broker_url, backend=celery_backend_url)
except Exception as e:
    raise e


@after_setup_logger.connect
def setup_celery_logger(logger, *args, **kwargs):
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger("tasks")
    fh = logging.FileHandler("logs/tasks.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)


@celery.task(name="push_notification")
def push_notification(input_token: str):
    time.sleep(5)
    logger.info(f"Sending notification to {input_token} as part of celery task")
    return {"result": f"Notification sent to {input_token}"}
