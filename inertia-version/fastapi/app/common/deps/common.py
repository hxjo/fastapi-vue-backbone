from dataclasses import dataclass
from typing import Annotated, Any

from fastapi import BackgroundTasks, Depends
from openfga_sdk import OpenFgaClient

from .fga import AnnotatedFGAClientDep
from .db import SessionDep
from .search import StructuredSearchClient, AnnotatedSearchClientsDep
from .tasks import TaskDep


@dataclass
class StructuredCommonDeps:
    session: SessionDep
    tasks: BackgroundTasks
    fga_client: OpenFgaClient
    search: StructuredSearchClient


def get_common_deps(
    *,
    session: SessionDep,
    task: Any = TaskDep,
    fga: AnnotatedFGAClientDep,
    search: AnnotatedSearchClientsDep,
) -> StructuredCommonDeps:
    return StructuredCommonDeps(
        session=session, tasks=task, fga_client=fga, search=search
    )


CommonDep = Depends(get_common_deps)
AnnotatedCommonDep = Annotated[StructuredCommonDeps, CommonDep]
