import logging
import os

os.makedirs(os.path.join(os.getcwd(), "logs"), exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)
