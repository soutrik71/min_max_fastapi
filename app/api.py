import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.tasks import push_notification

router = APIRouter(prefix="/notification", tags=["notification"])


@router.post("/send", status_code=202)
async def send_notification(input_token: str):
    task_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    try:
        results = push_notification.apply_async(
            (input_token,),
            task_id=task_id,
        )
        return JSONResponse(
            {
                "task_id": task_id,
                "status": True,
                "session_id": session_id,
            }
        )

    except Exception as e:
        print(e)

        return JSONResponse(
            {
                "status": False,
                "task_id": task_id,
                "error": str(e),
            }
        )
