import os

import uvicorn
from fastapi import FastAPI

from app.apis import tasks, user, weather
from app.logger import logging

logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(user.router)
app.include_router(weather.router)
app.include_router(tasks.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="info", reload=True)
