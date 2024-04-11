# Authorization

## Introduction
For authorization, we use OpenFGA, an implementation of Google's Zanzibar ReBAC (Relation Based Access Control) system. 
OpenFGA is a flexible and scalable system that allows us to define and enforce access control policies for our applications.

### The authorization model
The authorization model is stored in `authorization/model.fga`.
It uses OpenFGA DSL to define the authorization model.
Some poe commands are used to generate a JSON representation of the model, which is then used by the OpenFGA server to enforce access control policies.

### The store file
The store file, stored in `authorization/store.fga.yaml` is a simple representation of the authorization model.
It is used to write some tests on the model, and ensure that the model is correctly defined.

## How to implement authorization dependency in a route, or a router
In `app.modules.**.fga`, we define some classes which are meant to handle:
- Keeping the OpenFGA relations up-to-date with the database
- Checking the authorization of a user for a given resource

We rely on the dependency injection system of FastAPI to check if a user has the rights to perform an action on a resource.

### Step 1: Define the relationship in the model
In `authorization/model.fga`, define the relationship between the user and the resource.
For example, if you want to define a new book type in the model, you would write:
```text
type book
    relations
        define writer: [user]
        define can_update: writer
```

#### Step 1.1: Write some tests for it
In `authorization/store.fga.yaml`, write some tests for the new relationship.
```yaml
tests: 
  - name: "Book Permissions"
    description: "Only the writer of a book can update it"
    tuples:
      - user: user:someone
        relation: writer
        object: book:some_book

    check:
      - user: user:someone
        object: book:some_book
        assertions: 
          can_update: true
      - user: user:someone_else
        object: book:some_book
        assertions: 
          can_update: false
```

You can test those assertions by running the following command `poe cmd authz test-model`

#### Step 1.2: Generate the JSON representation of the model
Run `poe cmd authz model-to-json` to generate the JSON representation of the model.

#### Step 2: Write the new authorization model to the OpenFGA server
Run `poe cmd authz write-authorization-model` to write the new authorization model to the OpenFGA server.

#### Step 2: Alternative ; Do both in one command:
Run `poe cmd authz update` to cast the model to JSON and write it to the database.

### Step 3: Create the class to handle the relationship creation / deletion
In `app.modules.book.fga`, create a class to handle the relationship between the user and the book.
```python
from openfga_sdk.client.models.tuple import ClientTuple
from openfga_sdk.client.models.write_request import ClientWriteRequest
from openfga_sdk.sync import OpenFgaClient

class BookFGA:

    @staticmethod
    def get_tuple_user_on_book(id_: int, user_id: int) -> ClientTuple:
        return ClientTuple(
            user=f"user:{user_id}",
            relation="writer",
            object=f"book:{id_}",
        )

    @classmethod
    def create_book_relationships(
        cls, fga_client: OpenFgaClient, id_: int, user_id: int
    ):
        body = ClientWriteRequest(
            writes=[
                cls.get_tuple_user_on_book(id_, user_id),
            ],
        )
        fga_client.write(body)

    @classmethod
    def delete_book_relationships(
        cls, fga_client: OpenFgaClient, id_: int, user_id: int
    ):
        body = ClientWriteRequest(
            deletes=[
                cls.get_tuple_user_on_book(id_, user_id),
            ],
        )
        fga_client.write(body)
```

Now, we have a class to handle the creation and deletion of the relationship between a user and a book.  
You can now create a CRUD class for the book, and use those methods to create and delete the relationships,
in the callbacks of the CRUD class.
Notice we're using FastAPI's BackgroundTasks to handle the creation and deletion of the relationships in the background.
They will be handled asynchronously, even once the response is sent to the client.

`app.modules.book.repository`
```python
from typing import cast

from app.common.repository import BaseRepo
from .models import Book, BookCreate, BookUpdate  # noqa
from .fga import BookFGA  # noqa


class BookRepo(BaseRepo[Book, BookCreate, BookUpdate]):
    @classmethod
    def callback_create(cls, db_obj: Book, *, tasks, fga_client) -> None:
        book_id = cast(int, db_obj.id)
        tasks.add_task(
            BookFGA.create_book_relationships,
            fga_client,
            book_id,
            db_obj.writer_id,
        )

    @classmethod
    def callback_delete(cls, db_obj: Book, *, tasks, fga_client) -> None:
        book_id = cast(int, db_obj.id)
        tasks.add_task(
            BookFGA.delete_book_relationships,
            fga_client,
            book_id,
            db_obj.writer_id,
        )
```

Notice we're using `typing`'s `cast` to cast the `db_obj.id` to `int`.

This is due to the fact that the Book object represents a database object and is used for insertion too.
Therefore, it doesn't have an `id` attribute, and we need to cast it to `int` to access it.
This is a common pattern in the CRUD classes.


### Step 4: Update the class to allow for checks on the authorization
In `app.modules.book.fga`, update the class to allow for checks on the authorization.
```python
from typing import Literal

from openfga_sdk.client.models.check_request import ClientCheckRequest
from openfga_sdk.sync import OpenFgaClient

AllowedBookRelations = Literal[
    "can_update",
]

class BookFGA:
    # ... Rest of the class
    @staticmethod
    def has_user_relationship(
        user_id: int, relationship: AllowedBookRelations, book_id: int
    ) -> ClientCheckRequest:
        return ClientCheckRequest(
            user=f"user:{user_id}",
            relation=relationship,
            object=f"book:{book_id}",
        )
    # ... Rest of the class
    @classmethod
    def can_update_book(
        cls, fga_client: OpenFgaClient, user_id: int, book_id: int
    ) -> bool:
        body = cls.has_user_relationship(user_id, "can_update", book_id)
        response = fga_client.check(body)
        return response.allowed

```

### Step 5: Create a dependency to check the authorization
In `app.modules.book.deps`, create a dependency to check if the user has the rights to perform an action on a book.

```python
from fastapi import Depends

from app.common.exceptions import ForbiddenException
from app.auth.deps import CurrentUserDep
from app.common.deps import FGAClientDep
from .fga import BookFGA  # noqa


def current_can_update_book(
        book_id: int, *, current_user=CurrentUserDep, fga_client=FGAClientDep
) -> None:
    if not BookFGA.can_update_book(fga_client, book_id, current_user.id):
        raise ForbiddenException(target="book")


CurrentCanUpdateBookDep = Depends(current_can_update_book)
```


### Step 6: Use the dependency in the route
In `app.modules.book.api_v1`, use the dependency in the route.

```python
from fastapi import APIRouter

from app.common.deps.common import AnnotatedCommonDep
from .deps import CurrentCanUpdateBookDep  # noqa
from .repository import BookRepo  # noqa
from .models import BookOut, BookUpdate  # noqa

router = APIRouter()


@router.patch(
    "/{book_id}",
    response_model=BookOut,
    status_code=201,
    dependencies=[CurrentCanUpdateBookDep],
)
async def update_book(
        book_id: int,
        book: BookUpdate,
        *,
        deps: AnnotatedCommonDep
):
    return BookRepo.update(deps, id_=book_id, obj_in=book)

```


### Step 7: Write a test for it
In `modules.book.tests.factory` create a factory for the book.

```python
from typing import cast

from openfga_sdk.sync import OpenFgaClient
from sqlmodel import Session

from .fga import BookFGA  # noqa
from .models import Book  # noqa
from app.user.models import User

from app.user.tests.factory import new_default_user
from app.common.test_utils.utils import random_lower_string


def new_book(session: Session, fga_client: OpenFgaClient, **kwargs) -> Book:
    book = Book(**kwargs)
    session.add(book)
    session.commit()
    session.refresh(book)
    book_id = cast(int, book.id)
    BookFGA.create_relationships(fga_client, book_id, book.writer_id)
    return book


def new_default_book(
        session: Session,
        fga_client: OpenFgaClient,
        *,
        writer: User | None = None,
        name: str | None = None,
):
    return new_book(
        session,
        fga_client,
        name=name or random_lower_string(),
        writer=writer or new_default_user(session=session, fga_client=fga_client),
    )

```

In `app.common.test_utils.factory` Add your new factory to the class:
```python
from app.modules.book.models import Book  # noqa
from app.tests.utils.factories.book import new_default_book  # noqa

class Factory:
    tuple_models_methods = [..., (Book, "create_book")]
    ...
    @classmethod
    async def create_book(cls, session, fga_client, search_clients, **kwargs):
        return await new_default_book(session, fga_client, search_clients, **kwargs)


```

In `app.modules.book.tests.test_api_v1`, write a test for the new route.

```python
from app.common.test_utils.utils import authenticate_client, get_route
from app.modules.book.api_v1 import update_book  # noqa
from app.modules.book.models import Book  # noqa
from app.user.models import User

# factory and client are fixtures defined in conftest.py. They are available in all tests.

async def test_writer_can_update_book(client, factory):
    user = await factory(User)
    book = await factory(Book, writer=user)
    authenticate_client(client, user)
    response = client.patch(
        get_route(update_book, book_id=book.id),
        json={"name": "new name"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "new name"

    
async def test_other_user_cannot_update_book(client, factory):
    user = await factory(User)
    book = await factory(Book)
    authenticate_client(client, user)
    response = client.patch(
        get_route(update_book, book_id=book.id),
        json={"name": "new name"},
    )
    assert response.status_code == 403
```