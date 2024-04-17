import asyncio

import typer
from rich.prompt import IntPrompt, Prompt
from sqlmodel import Session, select

from app.core.sync_db import engine
from app.auth.utils.auth import get_password_hash
from app.user.models import User
from app.user.fga import UserFGA

from .authz import get_fga_client_config
from openfga_sdk import OpenFgaClient
from .options import Option, handle_options
from .print import print_error, print_info, print_success

app = typer.Typer()


@app.command()
def create_superuser() -> None:
    """
    Create a new superuser
    """
    asyncio.run(async_create_superuser())


async def async_create_superuser():
    """
    Create a new superuser
    """
    print_info("Please provide the following information")
    email = Prompt.ask("Email address")
    username = Prompt.ask("Username")
    password = Prompt.ask("Password")
    session = Session(engine)
    user = User(
        email=email,
        username=username,
        hashed_password=get_password_hash(password),
        is_active=True,
        is_superuser=True,
        avatar_url=None,
    )
    session.add(user)
    session.commit()
    print_success(f"Superuser created successfully with id {user.id}")
    config = get_fga_client_config()
    async with OpenFgaClient(config) as fga_client:
        await UserFGA.create_relationships(fga_client, user.id, "superuser")


@app.command()
def set_superuser() -> None:
    asyncio.run(async_set_superuser())


async def async_set_superuser() -> None:
    """
    Set a user as superuser
    """
    session = Session(engine)
    opts = IntPrompt.ask(
        "Do you want to provide an id (1) or an email (2)?", choices=["1", "2"]
    )

    match opts:
        case 1:
            user_id = IntPrompt.ask("Enter the user id")
            stmt = select(User).where(User.id == user_id)
            user = session.exec(stmt).first()
            if user is None:
                print_error("User not found")
                return set_superuser()
            user.is_superuser = True
            session.commit()
            print_success("User is now a superuser")
        case 2:
            email = Prompt.ask("Enter the user email")
            stmt = select(User).where(User.email == email)
            user = session.exec(stmt).first()
            if user is None:
                print_error("User not found")
                return set_superuser()
            user.is_superuser = True
            session.commit()
            print_success("User is now a superuser")
    config = get_fga_client_config()
    async with OpenFgaClient(config) as fga_client:
        await UserFGA.create_relationships(fga_client, user.id, "superuser")


@app.command()
def i(allow_back: bool = False):
    """
    Interactive mode
    """
    handle_options(
        [
            Option(index=1, description="Create a superuser", func=create_superuser),
            Option(index=2, description="Set a user as superuser", func=set_superuser),
        ],
        allow_back=allow_back,
    )


if __name__ == "__main__":
    app()
