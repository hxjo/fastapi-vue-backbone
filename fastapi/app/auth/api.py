from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.auth.models import NewPassword, Token
from app.auth.utils.auth import (
    generate_password_reset_token,
    verify_password_reset_token,
)
from app.auth.utils.email import send_reset_password_email
from app.common.deps.common import AnnotatedCommonDep
from app.common.deps.db import SessionDep
from app.common.exceptions import BadRequestException
from app.core.config import settings
from app.user.models import UserOut
from app.user.repository import UserRepo

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], *, session: SessionDep
):
    return await UserRepo.authenticate(
        session, email=form_data.username, password=form_data.password
    )


@router.post("/password/recovery/{email}", status_code=204)
async def recover_password(email: str, *, session: SessionDep):
    user = await UserRepo.get_by_email(
        session, email=email
    )  # Raise if not found in the DB
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, username=user.username, token=password_reset_token
    )


@router.post("/reset-password/", status_code=201, response_model=UserOut)
async def reset_password(body: NewPassword, *, deps: AnnotatedCommonDep):
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    user = await UserRepo.get_by_email(deps.session, email=email)
    if not user.is_active or not isinstance(user.id, int):
        raise BadRequestException(target="user", additional_info="inactive")

    return UserRepo.update(deps, id_=user.id, obj_in={"password": body.password})


templates = Jinja2Templates(directory="app/utils")


@router.get("/recover-password")
async def recover_password_view(request: Request, token: str):
    return templates.TemplateResponse(
        "reset_password_template.html",
        {"request": request, "token": token, "project_name": settings.PROJECT_NAME},
    )
