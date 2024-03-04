import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    broker_host_name: str = os.getenv("BROKER_HOST_NAME", "localhost")
    broker_port: int = os.getenv("BROKER_PORT", 6379)


celery_broker_url = f"redis://{Settings().broker_host_name}:{Settings().broker_port}/0"
celery_backend_url = f"redis://{Settings().broker_host_name}:{Settings().broker_port}/0"


if __name__ == "__main__":
    print(celery_broker_url)
    print(celery_backend_url)
