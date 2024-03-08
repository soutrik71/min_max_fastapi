from celery import Celery

from app.broker_test import test_celery_broker_url
from app.settings import celery_backend_url, celery_broker_url

try:
    test_celery_broker_url()
    celery = Celery(
        __name__,
        broker=celery_broker_url,
        backend=celery_backend_url,
        task_track_started=True,
    )
except Exception as e:
    raise e
