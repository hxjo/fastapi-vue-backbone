from fastapi import APIRouter
from app.common.deps.inertia import InertiaDep
from inertia import InertiaResponse
from app.auth.deps import AnnotatedCurrentUserDep, AnnotatedCurrentUserOrNoneDep
from app.user.models import UserOut

webapp_router = APIRouter()


@webapp_router.get("/", response_model=None)
async def index(
    inertia: InertiaDep, maybe_user: AnnotatedCurrentUserOrNoneDep
) -> InertiaResponse:
    user = UserOut.from_orm(maybe_user) if maybe_user else None
    return await inertia.render(
        "HomeView",
        {
            "user": user,
        },
    )


@webapp_router.get("/app", response_model=None)
async def app(inertia: InertiaDep, user: AnnotatedCurrentUserDep) -> InertiaResponse:
    user_ = UserOut.from_orm(user).model_dump()
    return await inertia.render("AppView", {"user": user_})
