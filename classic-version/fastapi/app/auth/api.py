from typing import Annotated, cast

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.models import NewPassword
from app.auth.utils.auth import (
    generate_password_reset_token,
    verify_password_reset_token,
)
from app.auth.utils.email import send_reset_password_email
from app.common.deps.common import AnnotatedCommonDep
from app.common.deps.db import SessionDep
from app.common.exceptions import BadRequestException
from app.user.models import UserAndToken, UserOut
from app.user.repository import UserRepo

router = APIRouter()


@router.post("/api/login", response_model=UserAndToken)
async def api_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], *, session: SessionDep
):
    token = await UserRepo.authenticate(
        session, email=form_data.username, password=form_data.password
    )
    user = await UserRepo.get_by_email(session, email=form_data.username)
    return UserAndToken(
        user=UserOut.model_validate(user),
        token=token,
    )


@router.post("/api/recover-password/{email}", status_code=204)
async def send_recover_password_email(email: str, *, session: SessionDep):
    user = await UserRepo.get_by_email(
        session, email=email
    )  # Raise if not found in the DB
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, username=user.username, token=password_reset_token
    )


@router.post("/api/reset-password/", status_code=201, response_model=UserOut)
async def reset_password(body: NewPassword, *, deps: AnnotatedCommonDep):
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    user = await UserRepo.get_by_email(deps.session, email=email)
    if not user.is_active:
        raise BadRequestException(target="user", additional_info="inactive")
    user_id = cast(int, user.id)
    return await UserRepo.update(deps, id_=user_id, obj_in={"password": body.password})
