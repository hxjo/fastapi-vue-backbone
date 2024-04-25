import subprocess

import typer
from dotenv import load_dotenv

from .processes import run_apps
from .search_commands.update import update_indexes_if_needed
from .docker import up, migrate_db
from .authz import (
    setup_store,
    write_authorization_model,
    is_first_time,
    has_authorization_model_changed,
)
from .print import print_info, print_success


def run(up_services: bool = True, host: str = "0.0.0.0", port: int = 8000) -> None:
    if up_services:
        up()
    migrate_db()
    update_indexes_if_needed()
    load_dotenv(override=True)
    if is_first_time():
        setup_store()
    if has_authorization_model_changed():
        print_info("Updating the OpenFGA model...")
        write_authorization_model()
    if is_first_time():
        print_info("Migrating seeding data...")
        subprocess.run(["poe", "cmd", "authz", "migrate-existing-data"], check=True)

    print_success("Update complete!")

    print_info("Running the app...")
    run_apps(host, port)


if __name__ == "__main__":
    typer.run(run)
