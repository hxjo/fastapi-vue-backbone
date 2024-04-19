from datetime import datetime, timezone
from typing import Annotated, cast

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from app.auth.deps import RedirectIfAlreadyLoggedInDep
from app.auth.exceptions import InvalidCredentialsException, InvalidTokenException
from app.auth.models import NewPassword
from app.auth.utils.auth import (
    add_token_to_response,
    generate_password_reset_token,
    verify_password_reset_token,
)
from app.auth.utils.email import send_reset_password_email
from app.common.deps.common import AnnotatedCommonDep
from app.common.deps.db import SessionDep
from app.common.deps.inertia import InertiaDep
from app.common.exceptions import BadRequestException, NotFoundException
from app.libs.inertia import InertiaResponse
from app.user.repository import UserRepo

router = APIRouter()


@router.get(
    "/signup", dependencies=[RedirectIfAlreadyLoggedInDep], include_in_schema=False, response_model=None
)
async def signup(inertia: InertiaDep) -> InertiaResponse:
    return await inertia.render("auth/SignupView")


@router.get(
    "/login", dependencies=[RedirectIfAlreadyLoggedInDep], include_in_schema=False, response_model=None
)
async def login(inertia: InertiaDep) -> InertiaResponse:
    return await inertia.render("auth/LoginView")


@router.post("/api/login", response_model=None)
async def api_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], *, session: SessionDep, inertia: InertiaDep
) -> RedirectResponse:
    try:
        token = await UserRepo.authenticate(
            session, email=form_data.username, password=form_data.password
        )
        response = RedirectResponse(url="/app", status_code=303)
        response = add_token_to_response(response, token=token.access_token)
        return response
    except InvalidCredentialsException as exc:
        response = RedirectResponse(url="/login", status_code=303)
        inertia.flash(exc.message, category="error")
        return response


@router.get("/logout", response_model=None)
async def logout() -> RedirectResponse:
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


@router.post("/api/recover-password/{email}", status_code=204, response_model=None)
async def send_recover_password_email(email: str, *, session: SessionDep, inertia: InertiaDep) -> RedirectResponse:
    response = RedirectResponse(url="/recover-password", status_code=303)
    try:
        user = await UserRepo.get_by_email(
            session, email=email
        )  # Raise if not found in the DB
        password_reset_token = generate_password_reset_token(email=email)
        send_reset_password_email(
            email_to=user.email, username=user.username, token=password_reset_token
        )
        inertia.flash("auth.recovery_email_sent", category="message")
    except NotFoundException as exc:
        inertia.flash(exc.message, category="error")
    return response


@router.post("/api/reset-password/", status_code=201, response_model=None)
async def reset_password(body: NewPassword, *, deps: AnnotatedCommonDep, inertia: InertiaDep) -> RedirectResponse:
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
        inertia.flash(exc.message, category="error")
        return response
    user_id = cast(int, user.id)
    await UserRepo.update(deps, id_=user_id, obj_in={"password": body.password})
    response = RedirectResponse(url="/app", status_code=303)
    inertia.flash("auth.password_reset_success", category="message")
    response = add_token_to_response(response, email=email)
    return response


templates = Jinja2Templates(directory="app/utils")


@router.get(
    "/recover-password",
    dependencies=[RedirectIfAlreadyLoggedInDep],
    include_in_schema=False,
    response_model=None
)
async def recover_password_view(inertia: InertiaDep) -> InertiaResponse:
    return await inertia.render("auth/RecoverPasswordView")


@router.get(
    "/reset-password",
    dependencies=[RedirectIfAlreadyLoggedInDep],
    include_in_schema=False,
    response_model=None
)
async def reset_password_view(inertia: InertiaDep, token: str) -> InertiaResponse:
    try:
        email = verify_password_reset_token(token=token)
    except InvalidTokenException:
        email = None

    return await inertia.render("auth/ResetPasswordView", {"email": email, "token": token})

