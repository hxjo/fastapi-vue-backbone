import os
import subprocess
import typer
from dotenv import load_dotenv

from .search_commands.update import update_indexes_if_needed
from .docker import up, migrate_db
from .authz import setup_store, write_authorization_model, is_first_time
from .print import print_info, print_success


def run(up_services: bool = True, host: str = "0.0.0.0", port: int = 8000):
    if up_services:
        up()
    migrate_db()
    update_indexes_if_needed()
    load_dotenv(override=True)
    if is_first_time():
        setup_store()
    print_info("Updating the OpenFGA model...")
    write_authorization_model()
    print_info("Migrating the database...")
    if is_first_time():
        subprocess.run(["poe", "cmd", "authz", "migrate-existing-data"], check=True)

    print_success("Update complete!")

    print_info("Running the app...")
    app_port = os.getenv("FASTAPI_PORT", str(port))
    app_host = os.getenv("FASTAPI_HOST", host)
    subprocess.run(
        ["poe", "runapp", "--host", app_host, "--port", app_port], check=True
    )


if __name__ == "__main__":
    typer.run(run)
