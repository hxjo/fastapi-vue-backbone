from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from app.user.search import UserSearch


@dataclass
class StructuredSearchClient:
    user: UserSearch


def get_search_clients() -> StructuredSearchClient:
    return StructuredSearchClient(
        user=UserSearch(),
    )


SearchClientsDep = Depends(get_search_clients)
AnnotatedSearchClientsDep = Annotated[StructuredSearchClient, SearchClientsDep]
