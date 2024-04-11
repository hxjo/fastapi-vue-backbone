# Authentication

## How to implement authentication dependency in a route, or a router

### Router-level authentication dependency
If you need a whole router to be under an authentication dependency, you can include it as such:
`app.api.v1`

```python
from fastapi import APIRouter
from app.auth.deps import CurrentUserDep
from app.modules.book.api_v1 import router as book_router  # noqa

api_router_v1 = APIRouter()
api_router_v1.include_router(
    book_router,
    prefix="/books",
    tags=["books"],
    dependencies=[CurrentUserDep],
)
```

### Route-level authentication dependency
If you need to put an authentication dependency on only one (or a few) routes, you can define it as such:
`app.modules.book.api_v1`

```python
from fastapi import APIRouter
from app.auth.deps import CurrentUserDep

router = APIRouter()


@router.get("/{book_id}", dependencies=[CurrentUserDep])
async def get_book():
    # Do your logic here
    # You won't have access to the current user, but this ensures that the user is indeed authenticated, exists and 
    # that the token is not expired
    pass
```

### Access to currently authenticated user
Sometimes, you'll have to know who is performing the action to know if they have the right to do so. Here is
how you can have access to it:
`app.modules.book.api_v1`

```python
from fastapi import APIRouter
from app.auth.deps import AnnotatedCurrentUserDep
from app.common.exceptions import ForbiddenException

router = APIRouter()


@router.put(
    "/{book_id}",
    status_code=201,
)
async def update_user(
        book_id: int,
        current_user: AnnotatedCurrentUserDep,
        # This acts both as a verification for the token and as a getter for the current user.
):
    if book_id not in current_user.book_ids:
        raise ForbiddenException(target="user")
```
