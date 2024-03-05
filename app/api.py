import logging
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.tasks import push_notification

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/notification", tags=["notification"])


@router.post("/send", status_code=202)
async def send_notification(input_token: str):
    task_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    logger.info(
        f"Task ID: {task_id} - Session ID: {session_id} - Sending notification to {input_token} from api side"
    )
    try:
        results = push_notification.apply_async(
            (input_token,),
            task_id=task_id,
        )
        logger.info(
            f"Task ID: {task_id} - Session ID: {session_id} - Task {results.id} completed successfully"
        )
        return JSONResponse(
            {
                "task_id": task_id,
                "status": True,
                "session_id": session_id,
            }
        )

    except Exception as e:
        logger.exception(
            f"Task ID: {task_id} - Session ID: {session_id} - Error: {str(e)}"
        )

        return JSONResponse(
            {
                "status": False,
                "task_id": task_id,
                "error": str(e),
            }
        )


@router.get("/status/{task_id}", status_code=200)
async def task_status(task_id: str):
    try:
        task = push_notification.AsyncResult(task_id)
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
