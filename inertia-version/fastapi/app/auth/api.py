from datetime import datetime, timedelta, timezone
from typing import Annotated, cast

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from app.auth.deps import RedirectIfAlreadyLoggedInDep
from app.auth.exceptions import InvalidCredentialsException, InvalidTokenException
from app.auth.models import NewPassword
from app.auth.utils.auth import (
    create_access_token,
    generate_password_reset_token,
    verify_password_reset_token,
)
from app.auth.utils.email import send_reset_password_email
from app.common.deps.common import AnnotatedCommonDep
from app.common.deps.db import SessionDep
from app.common.exceptions import BadRequestException, NotFoundException
from app.core.config import settings
from app.libs.inertia import inertia
from app.user.models import UserOut
from app.user.repository import UserRepo
from app.webapp.models import Message, MessageOut

router = APIRouter()


@router.get(
    "/signup", dependencies=[RedirectIfAlreadyLoggedInDep], include_in_schema=False
)
@inertia("auth/SignupView")
async def signup(request: Request):
    error = request.cookies.get("error", None)
    if error is not None:
        return MessageOut(
            message=Message(
                content=error, timestamp=datetime.now().timestamp(), type="error"
            )
        ).model_dump()
    return {}


@router.get(
    "/login", dependencies=[RedirectIfAlreadyLoggedInDep], include_in_schema=False
)
@inertia("auth/LoginView")
async def login(request: Request):
    error = request.cookies.get("error", None)
    if error is not None:
        return MessageOut(
            message=Message(
                content=error, timestamp=datetime.now().timestamp(), type="error"
            )
        ).model_dump()
    return {}


@router.post("/api/login")
async def api_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], *, session: SessionDep
):
    try:
        token = await UserRepo.authenticate(
            session, email=form_data.username, password=form_data.password
        )
        response = RedirectResponse(url="/app", status_code=303)
        response.set_cookie(
            key="token",
            value=token.access_token,
            httponly=True,
            samesite=None,
            secure=True,
            expires=datetime.now(timezone.utc)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return response
    except InvalidCredentialsException as exc:
        response = RedirectResponse(url="/login", status_code=303)
        response.set_cookie(
            "error", exc.message, path="/", samesite=None, secure=True, expires=3
        )
        return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        "token",
        "deleted",
        path="/",
        expires=datetime.min.replace(tzinfo=timezone.utc),
        samesite=None,
        secure=True,
        httponly=True,
    )
    return response


@router.post("/api/recover-password/{email}", status_code=204)
async def send_recover_password_email(email: str, *, session: SessionDep):
    response = RedirectResponse(url="/recover-password", status_code=303)
    try:
        user = await UserRepo.get_by_email(
            session, email=email
        )  # Raise if not found in the DB
        password_reset_token = generate_password_reset_token(email=email)
        send_reset_password_email(
            email_to=user.email, username=user.username, token=password_reset_token
        )
        response.set_cookie(
            "message",
            "auth.recovery_email_sent",
            path="/",
            samesite=None,
            secure=True,
            expires=3,
        )
    except NotFoundException as exc:
        response.set_cookie(
            "error", exc.message, path="/", samesite=None, secure=True, expires=3
        )
    return response


@router.post("/api/reset-password/", status_code=201, response_model=UserOut)
async def reset_password(body: NewPassword, *, deps: AnnotatedCommonDep):
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    user = await UserRepo.get_by_email(deps.session, email=email)
    if not user.is_active:
        exc = BadRequestException(target="user", additional_info="inactive")
        response = RedirectResponse(
            f"/reset-password?token={body.token}", status_code=303
        )
        response.set_cookie(
            "error", exc.message, path="/", samesite=None, secure=True, expires=3
        )
        return response
    user_id = cast(int, user.id)
    await UserRepo.update(deps, id_=user_id, obj_in={"password": body.password})
    access_token = create_access_token(
        data={"email": user.email},
    )
    response = RedirectResponse(url="/app", status_code=303)
    response.set_cookie(
        key="message",
        value="auth.password_reset_success",
        path="/",
        samesite=None,
        secure=True,
        expires=3,
    )
    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        samesite=None,
        secure=True,
        expires=datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return response


templates = Jinja2Templates(directory="app/utils")


@router.get(
    "/recover-password",
    dependencies=[RedirectIfAlreadyLoggedInDep],
    include_in_schema=False,
)
@inertia("auth/RecoverPasswordView")
async def recover_password_view(request: Request):
    error = request.cookies.get("error", None)
    message = request.cookies.get("message", None)
    if error is not None:
        return MessageOut(
            message=Message(
                content=error, timestamp=datetime.now().timestamp(), type="error"
            )
        ).model_dump()
    if message is not None:
        return MessageOut(
            message=Message(
                content=message,
                timestamp=datetime.now().timestamp(),
            )
        ).model_dump()
    return {}


@router.get(
    "/reset-password",
    dependencies=[RedirectIfAlreadyLoggedInDep],
    include_in_schema=False,
)
@inertia("auth/ResetPasswordView")
async def reset_password_view(request: Request, token: str):
    try:
        email = verify_password_reset_token(token=token)
    except InvalidTokenException:
        email = None
    error = request.cookies.get("error", None)
    message = request.cookies.get("message", None)
    if error is not None:
        return MessageOut(
            message=Message(
                content=error, timestamp=datetime.now().timestamp(), type="error"
            )
        ).model_dump()
    if message is not None:
        return MessageOut(
            message=Message(
                content=message,
                timestamp=datetime.now().timestamp(),
            )
        ).model_dump()
    return {
        "email": email,
        "token": token,
    }
