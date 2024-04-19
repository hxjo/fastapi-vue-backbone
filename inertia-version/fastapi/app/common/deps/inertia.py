from typing import Annotated
from fastapi import Depends
from app.libs.inertia import InertiaRenderer, inertia_renderer_factory, InertiaConfig

InertiaDep = Annotated[
    InertiaRenderer, Depends(inertia_renderer_factory(InertiaConfig()))
]