from typing import Any

from fastapi import APIRouter, Request

from app.libs.inertia import inertia


inertia_router = APIRouter()


@inertia_router.get("/")
@inertia("HomeView")
async def index(request: Request) -> dict[str, Any]:
    return {"message": "Hello world from the index !"}


@inertia_router.get("/about")
@inertia("AboutView")
async def about(request: Request) -> dict[str, Any]:
    return {"message": "Hello world from the about page !"}
