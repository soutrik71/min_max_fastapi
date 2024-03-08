import asyncio

from celery import shared_task, states
from celery.exceptions import Ignore
from celery.utils.log import get_task_logger
from fastapi.responses import JSONResponse

from app.worker import celery
from engine.dummy_methods import method1, method2, method3

logger = get_task_logger("tasks")


@celery.task(name="push_notification", bind=True, retry_kwargs={"max_retries": 3})
def push_notification(self, input_token: str):
    logger.info(f"Sending notification to {input_token} as part of celery task")
    start = 0
    op1 = asyncio.run(method1(input_token))
    self.update_state(state="PROGRESS", meta={"output": op1})
    op2 = asyncio.run(method2(input_token))
    self.update_state(state="PROGRESS", meta={"output": op2})
    op3 = asyncio.run(method3(input_token))
    self.update_state(state=states.SUCCESS, meta={"output": op3, "result": op3})
    raise Ignore()

    return {"result": op3}
