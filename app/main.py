import os

import uvicorn
from fastapi import FastAPI

from app import api
from app.logger import logging

logger = logging.getLogger(__name__)

logging.info(f"Starting FastAPI app from path {os.getcwd()} ")

app = FastAPI()
app.include_router(api.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="info", reload=True)
