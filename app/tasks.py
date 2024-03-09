import asyncio
import os

import requests
from celery import shared_task, states
from celery.exceptions import Ignore
from celery.utils.log import get_task_logger
from fastapi.responses import JSONResponse

from app.crud import (
    crud_add_nested,
    crud_add_user,
    crud_add_weather,
    crud_update_nested,
)
from app.schemas import NestedIn, UserIn, WeatherIn
from app.worker import celery
from engine.methods import method1, method2, method3

logger = get_task_logger(__name__)


@celery.task(name="task_add_user", bind=True, retry_kwargs={"max_retries": 3})
def task_add_user(count: int):
    url = "https://randomuser.me/api"
    response = requests.get(f"{url}?results={count}").json()["results"]
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


@celery.task(name="task_add_weather", bind=True, retry_kwargs={"max_retries": 3})
def task_add_weather(city: str):
    url = "https://api.collectapi.com/weather/getWeather?data.lang=tr&data.city="
    headers = {
        "content-type": "application/json",
        "authorization": "apikey 4HKS8SXTYAsGz45l4yIo9P:0NVczbcuJfjQb8PW7hQV48",
    }
    response = requests.get(f"{url}{city}", headers=headers).json()["result"]
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


@celery.task(name="nested_application", bind=True, retry_kwargs={"max_retries": 3})
def nested_application(self, input_token: str):
    logger.info(f"Sending notification to {input_token} as part of celery task")
    nested = crud_update_nested(NestedIn(input_token=input_token))
    # task1
    op1 = asyncio.run(method1(input_token))
    self.update_state(state="PROGRESS", meta={"output": op1})
    nested = NestedIn(input_token=input_token, output=op1)
    crud_update_nested(nested)
    # task2
    op2 = asyncio.run(method2(input_token))
    self.update_state(state="PROGRESS", meta={"output": op2})
    nested = NestedIn(input_token=input_token, output=op2)
    crud_update_nested(nested)

    # task3
    op3 = asyncio.run(method3(input_token))
    self.update_state(state=states.SUCCESS, meta={"output": op3, "result": op3})
    raise Ignore()
