from redis import Redis

from app.settings import celery_broker_url


def test_celery_broker_url():
    redis_conn = Redis.from_url(celery_broker_url)
    if redis_conn.ping():
        print("Connection to broker established")
    else:
        raise ConnectionError("Connection to redis broker failed")


if __name__ == "__main__":
    test_celery_broker_url()
