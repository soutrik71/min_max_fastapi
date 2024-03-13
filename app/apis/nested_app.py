import logging

from celery.result import AsyncResult
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.crud import crud_error_message, crud_add_nested
from app.tasks import nested_application
import uuid
from app.schemas import NestedIn
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/nested", tags=["nested"])

@router.post("/app", status_code=201):
def nested_app(input_token):
    """
    Nested application.
    """
    logger.info(f"Nested application")
    chat_id = str(uuid.uuid4())
    _ = nested_application.apply_async((input_token,), task_id=chat_id)
    _ = crud_add_nested(NestedIn(input_token=input_token, chat_id=chat_id))
    return JSONResponse({"chat_id": chat_id,"input_token": input_token})
    