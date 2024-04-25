from fastapi.responses import Response
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, TypeVar, Union, cast

import bcrypt
from jose import jwt
from jose.exceptions import JWTError

from app.auth.exceptions import InvalidTokenException
from app.core.config import settings


def create_access_token(
    data: Dict[str, Any],
    expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    """
    Encodes data in an access token and returns it
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_token_content(token: str) -> Dict[str, Any]:
    """
    Decode a JWT token or raise JWTError
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def get_password_hash(password: str) -> str:
    """
    Encodes a password and returns its hash
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password_against_hash(password: str, hashed_password: str) -> bool:
    """
    Returns a boolean indicating if the password matches the hashed password
    """
    return bcrypt.checkpw(
        password=password.encode(), hashed_password=hashed_password.encode()
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "email": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return cast(str, decoded_token["email"])
    except JWTError as exc:
        raise InvalidTokenException() from exc


ResponseType = TypeVar("ResponseType", bound=Response)


def add_token_to_response(
    response: ResponseType,
    *,
    email: Union[str, None] = None,
    token: Union[str, None] = None,
) -> ResponseType:
    token = create_access_token(data={"email": email}) if token is None else token
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        samesite=None,
        secure=True,
        expires=datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return response
