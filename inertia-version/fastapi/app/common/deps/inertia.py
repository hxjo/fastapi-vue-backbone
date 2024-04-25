import subprocess
import os
from fastapi import Depends
from typing import Annotated
from app.core.config import settings

from inertia import Inertia, InertiaConfig, inertia_dependency_factory

manifest_json = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "..",
    "vue",
    "dist",
    "client",
    "manifest.json",
)


def get_git_revision_short_hash() -> str:
    return (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .decode("ascii")
        .strip()
    )


InertiaDep = Annotated[
    Inertia,
    Depends(
        inertia_dependency_factory(
            InertiaConfig(
                version=get_git_revision_short_hash(),
                manifest_json_path=manifest_json,
                use_typescript=True,
                environment=settings.ENVIRONMENT,
                use_flash_messages=True,
                use_flash_errors=True,
            )
        )
    ),
]
