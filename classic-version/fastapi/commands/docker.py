import os
import subprocess
import time
from typing import List

import typer
from dotenv import load_dotenv
from rich.prompt import Confirm

from .options import Option, handle_options
from .print import print_default, print_error, print_info, print_success

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
docker_compose_file = os.path.join(ABSOLUTE_PATH, "..", "..", "docker-compose.yml")
docker_compose_local_file = os.path.join(
    ABSOLUTE_PATH, "..", "..", "docker-compose.local.yml"
)

if os.path.isfile(docker_compose_local_file):
    DOCKER_COMPOSE_FILE = docker_compose_local_file
else:
    DOCKER_COMPOSE_FILE = docker_compose_file


load_dotenv()
if os.path.isfile(".env.local"):
    load_dotenv(dotenv_path=".env.local", override=True)

app = typer.Typer()


def exec_app(service: str, *, tty: bool = False) -> List[str]:
    process = ["docker", "exec"]
    if tty:
        process.append("-it")
    process.append(f"dine-in-vr-back-{service}-1")

    return process


@app.command()
def up():
    """
    Start the services
    """
    print_info("Upping the services...")
    try:
        subprocess.run(
            [
                "docker",
                "compose",
                "--file",
                DOCKER_COMPOSE_FILE,
                "up",
                "db",
                "minio",
                "mailhog",
                "meilisearch",
                "openfga",
                "openfga_db",
                "-d",
            ],
            check=True,
        )
        print_success("Services upped successfully!")

    except subprocess.CalledProcessError:
        print_error("An error occurred while upping the services")
        time.sleep(2)


@app.command()
def upall():
    """
    Start the services + the fastapi service
    """
    print_info("Upping the services and FastAPI...")
    try:
        subprocess.run(
            ["docker", "compose", "--file", DOCKER_COMPOSE_FILE, "up", "-d"], check=True
        )
        print_success("Services and FastAPI upped successfully!")
    except subprocess.CalledProcessError:
        print_error("An error occurred while upping the services and FastAPI")
        time.sleep(2)


@app.command()
def stop():
    """
    Stop the application
    """
    print_info("Stopping the application...")
    try:
        subprocess.run(
            ["docker", "compose", "--file", DOCKER_COMPOSE_FILE, "stop"], check=True
        )
        print_success("Application stopped successfully!")
    except subprocess.CalledProcessError:
        print_error("An error occurred while stopping the application")
        time.sleep(2)


@app.command()
def wipe(yes: bool = False):
    """
    Wipe the application
    """
    if yes or Confirm.ask("Are you sure you want to wipe the application ?"):
        try:
            subprocess.run(
                [
                    "docker",
                    "compose",
                    "--file",
                    DOCKER_COMPOSE_FILE,
                    "down",
                    "--volumes",
                    "--remove-orphans",
                    "--rmi",
                    "local",
                ],
                check=True,
            )
            print_success("Services wiped successfully!")
        except subprocess.CalledProcessError:
            print_error("An error occurred while wiping the application")
            time.sleep(2)


@app.command()
def psql():
    """
    Open a psql shell
    """
    print_info("Opening a psql shell...")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_db = os.getenv("POSTGRES_DB")
    exec_app_cmd = exec_app("db", tty=True)
    try:
        subprocess.run(
            [*exec_app_cmd, "psql", "-U", postgres_user, postgres_db], check=True
        )

    except subprocess.CalledProcessError:
        print_error("An error occurred while opening the psql shell")
        time.sleep(2)


@app.command()
def recreate_db():
    """
    Drop the database and recreate it
    """
    print_info("Recreating the database...")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_db = os.getenv("POSTGRES_DB")
    exec_app_cmd = exec_app("db", tty=True)
    try:
        subprocess.run(
            [*exec_app_cmd, "dropdb", "-U", postgres_user, postgres_db], check=True
        )
        print_default("Database dropped")
        subprocess.run(
            [*exec_app_cmd, "createdb", "-U", postgres_user, postgres_db], check=True
        )
        print_success("Database recreated")
        migrate_db()
    except subprocess.CalledProcessError:
        print_error("An error occurred while recreating the database")
        time.sleep(2)


@app.command()
def migrate_db():
    """
    Initialize the database: Migration + Seed
    """
    print_info("Migating the database...")
    try:
        subprocess.run(["poe", "migrate"], check=True)
        print_success("Database migrated successfully!")
    except subprocess.CalledProcessError as exc:
        print_error("An error occurred while migrating the database")
        time.sleep(2)
        raise exc


@app.command()
def first_setup():
    """
    First setup: Up + Init DB
    """
    up()
    migrate_db()


@app.command()
def i(allow_back: bool = False):
    """
    Interactive mode
    """
    handle_options(
        [
            Option(index=1, description="Start the application (up) 🚀", func=up),
            Option(index=2, description="Stop the application (stop) 🛑", func=stop),
            Option(index=3, description="Open a psql shell 🐘", func=psql),
            Option(
                index=4,
                description="Recreate the database (drop + create) 🔄",
                func=recreate_db,
            ),
            Option(
                index=5,
                description="Initialize the database (migrate + seed) 🌱",
                func=migrate_db,
            ),
            Option(
                index=6,
                description="First setup (up + init db) 🚀🌱",
                func=first_setup,
            ),
            Option(index=99, description="Wipe the application (down) 🧼", func=wipe),
        ],
        allow_back=allow_back,
    )


if __name__ == "__main__":
    app()
