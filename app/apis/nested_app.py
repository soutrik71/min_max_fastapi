import logging

from celery.result import AsyncResult
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.crud import crud_error_message, crud_get_user
from app.tasks import nested_application

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/nested", tags=["nested"])

@router