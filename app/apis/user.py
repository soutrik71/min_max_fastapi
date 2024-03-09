import logging

from celery.result import AsyncResult
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.crud import crud_error_message, crud_get_user
from app.tasks import task_add_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/user", tags=["users"])


@router.post("/users/{count}", status_code=201)
def add_user(count: int):
    """
    Get random user data from randomuser.me/api and
    add database using Celery. Uses Redis as Broker
    and Postgres as Backend.
    """
    logger.info(f"Adding {count} users")
    task = task_add_user.apply_async((count,))
    return {"task_id": task.id}


@router.post("/users/{count}", status_code=201)
def add_user_default_delay(count: int):
    """
    Get random user data from randomuser.me/api add
    database using Celery. Uses Redis as Broker
    and Postgres as Backend. (Delay = 10 sec)
    """
    logger.info(f"Adding {count} users")
    return add_user(count)


@router.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Get user from database.
    """
    logger.info(f"Getting user for id: {user_id}")
    user = crud_get_user(user_id)
    if user:
        return user
    else:
        raise HTTPException(404, crud_error_message(f"No user found for id: {user_id}"))
