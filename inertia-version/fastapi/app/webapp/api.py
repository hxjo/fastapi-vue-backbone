from datetime import datetime
from typing import Any

from fastapi import APIRouter, Request
from app.libs.inertia import inertia
from app.auth.deps import AnnotatedCurrentUserDep, AnnotatedCurrentUserOrNoneDep
from app.user.models import UserOut
from app.webapp.models import AppOut, HomeOut, Message

webapp_router = APIRouter()


@webapp_router.get("/")
@inertia("HomeView")
async def index(request: Request, maybe_user: AnnotatedCurrentUserOrNoneDep):
    user = UserOut.from_orm(maybe_user) if maybe_user else None
    return HomeOut(user=user).model_dump()


@webapp_router.get("/app")
@inertia("AppView")
async def app(request: Request, user: AnnotatedCurrentUserDep):
    message = request.cookies.get('message', None)
    message_: Message | None = None
    if message is not None:
        message_ = Message(
            content=message,
            timestamp=datetime.now().timestamp(),
        )

    return AppOut(user=UserOut.from_orm(user), message=message_).model_dump()

