from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.logger import logging
from app.settings import database_url

logger = logging.getLogger(__name__)

logger.info(f"Database URL: {database_url}")
engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
