import random
import string
from datetime import timedelta
from io import BytesIO
from typing import Any, Callable, Optional

from fastapi import UploadFile
from httpx import AsyncClient

from app.auth.utils.auth import create_access_token
from app.main import app


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def strong_password() -> str:
    lowercase = "".join(random.choices(string.ascii_lowercase, k=8))
    uppercase = "".join(random.choices(string.ascii_uppercase, k=8))
    digits = "".join(random.choices(string.digits, k=8))
    punctuation = "".join(random.choices(string.punctuation, k=8))

    return lowercase + uppercase + digits + punctuation


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_upload_file(filename: Optional[str] = None) -> UploadFile:
    _filename = filename if filename is not None else random_lower_string()
    dummy_content = _filename
    content_bytes = dummy_content.encode("utf-8")
    dummy_file = BytesIO(content_bytes)
    return UploadFile(filename=_filename, file=dummy_file)


def authenticate_client(
    client: AsyncClient, email: str, expires_minutes: Optional[int] = None
):
    token = create_access_token(
        {"email": email},
        expires_delta=timedelta(
            minutes=expires_minutes if expires_minutes is not None else 30
        ),
    )
    client.headers.update({"Authorization": f"Bearer {token}"})


def get_route(function: Callable[..., Any], **kwargs: Any) -> str:
    return app.url_path_for(function.__name__, **kwargs)
