import logging

from celery.result import AsyncResult
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.crud import crud_error_message, crud_get_weather
from app.tasks import task_add_weather

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/weather", tags=["weather"])


@router.post("/weathers/{city}", status_code=201)
def add_weather_default_delay(city: str):
    """
    Get weather data from api.collectapi.com/weather
    and add database using Celery. Uses Redis as Broker
    and Postgres as Backend. (Delay = 10 sec)
    """
    logger.info(f"Adding weather for city: {city}")
    return task_add_weather(city, 10)


@router.get("/weathers/{city}")
def get_weather(city: str):
    """
    Get weather from database.
    """
    logger.info(f"Getting weather for city: {city}")
    weather = crud_get_weather(city.lower())
    if weather:
        return weather
    else:
        raise HTTPException(
            404, crud_error_message(f"No weather found for city: {city}")
        )
