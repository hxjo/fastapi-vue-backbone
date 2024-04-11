from sqlmodel import Session, select  # noqa

from app.core.sync_db import engine
from app.user.models import *  # noqa
from app.auth.models import *  # noqa

from .print import print_info

session = Session(engine)

print_info("Welcome to the shell 🐚")
