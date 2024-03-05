# fastpi_celery
Application of simple Fast API with celery services

# Interaction of Client-API_Broker-Backend

![alt text](docs/image.png)


# Commands for running the application from local

## Celery Worker

```bash
(windows) --> celery -A app.tasks worker --pool=solo --prefetch-multiplier=1 --loglevel=info
(linux) --> celery -A app.celery_tasks worker --concurrency=1 --prefetch-multiplier=1 --loglevel=info --logfile=logs/celery.log
```

## Fast API

```bash
python -m uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8081
```