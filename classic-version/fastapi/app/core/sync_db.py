from sqlmodel import create_engine

from .config import settings

db_url = settings.SQLALCHEMY_SYNC_DATABASE_URI.unicode_string()  # type: ignore
engine = create_engine(db_url, echo=settings.DEBUG_SQL)
