import os
import time

import requests
from celery import Celery
from celery.utils.log import get_task_logger
from fastapi.responses import JSONResponse

from app.broker_test import test_celery_broker_url
from app.crud import crud_add_user, crud_add_weather
from app.schemas import UserIn, WeatherIn
from app.settings import celery_backend_url, celery_broker_url

logger = get_task_logger("tasks")

try:
    test_celery_broker_url()
    celery = Celery(__name__, broker=celery_broker_url, backend=celery_backend_url)
except Exception as e:
    raise e


@celery.task
def task_add_user(count: int, delay: int):
    url = "https://randomuser.me/api"
    response = requests.get(f"{url}?results={count}").json()["results"]
    time.sleep(delay)
    result = []
    for item in response:
        user = UserIn(
            first_name=item["name"]["first"],
            last_name=item["name"]["last"],
            mail=item["email"],
            age=item["dob"]["age"],
        )
        if crud_add_user(user):
            result.append(user.dict())
    return {"success": result}


@celery.celery
def task_add_weather(city: str, delay: int):
    url = "https://api.collectapi.com/weather/getWeather?data.lang=tr&data.city="
    headers = {
        "content-type": "application/json",
        "authorization": "apikey 4HKS8SXTYAsGz45l4yIo9P:0NVczbcuJfjQb8PW7hQV48",
    }
    response = requests.get(f"{url}{city}", headers=headers).json()["result"]
    time.sleep(delay)
    result = []
    for item in response:
        weather = WeatherIn(
            city=city.lower(),
            date=item["date"],
            day=item["day"],
            description=item["description"],
            degree=item["degree"],
        )
        if crud_add_weather(weather):
            result.append(weather.dict())
    return {"success": result}
