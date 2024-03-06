import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings
from sqlalchemy.engine import URL

load_dotenv()


class Settings(BaseSettings):
    broker_host_name: str = os.getenv("BROKER_HOST_NAME", "localhost")
    broker_port: int = os.getenv("BROKER_PORT", 6379)
    postgres_hostname: str = os.getenv("POSTGRES_HOSTNAME", "localhost")
    postgres_port: int = os.getenv("POSTGRES_PORT", 5432)
    postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    postgres_db: str = os.getenv("POSTGRES_DB", "postgres")
    postgres_driver: str = os.getenv("POSTGRES_DRIVER", "postgresql+psycopg2")


celery_broker_url = f"redis://{Settings().broker_host_name}:{Settings().broker_port}/0"
celery_backend_url = f"redis://{Settings().broker_host_name}:{Settings().broker_port}/0"
database_url = URL.create(
    drivername=Settings().postgres_driver,
    username=Settings().postgres_user,
    password=Settings().postgres_password,
    host=Settings().postgres_hostname,
    port=Settings().postgres_port,
    database=Settings().postgres_db,
)

if __name__ == "__main__":
    print(celery_broker_url)
    print(celery_backend_url)
    print(database_url)
