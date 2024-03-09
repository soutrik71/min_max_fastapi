import logging

from celery.result import AsyncResult
from fastapi import APIRouter
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
def read_root():
    """
    Developer: SC
    """
    return {"Chowdhury": "Soutrik"}


@router.get("/get_tasks/{task_id}")
def task_status(task_id: str):
    """
    Get task status.
    PENDING (waiting for execution or unknown task id)
    STARTED (task has been started)
    SUCCESS (task executed successfully)
    FAILURE (task execution resulted in exception)
    RETRY (task is being retried)
    REVOKED (task has been revoked)
    """
    try:
        task = AsyncResult(task_id)
        if task.state == "PENDING":
            response = {
                "task_id": task_id,
                "status": "PENDING",
            }
        elif task.state == "SUCCESS":
            response = {
                "task_id": task_id,
                "status": "SUCCESS",
                "result": task.result,
            }
        elif task.state == "PROGRESS":
            response = {
                "task_id": task_id,
                "status": "PROGRESS",
                "error": str(task.result),
            }
        elif task.state == "FAILURE":
            response = {
                "task_id": task_id,
                "status": "FAILURE",
                "error": str(task.result),
            }
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse(
            {
                "status": False,
                "task_id": task_id,
                "error": str(e),
            }
        )
