import subprocess
import typer
from dotenv import load_dotenv
from rich.prompt import Prompt
from .docker import up, upall, init_db
from .authz import setup_store, write_authorization_model
from .print import print_success

app = typer.Typer()


@app.command()
def setup():
    upall()
    setup_after_docker()


@app.command()
def setup_after_docker():
    init_db()
    setup_store()
    load_dotenv(override=True)
    write_authorization_model()
    load_dotenv(override=True)
    subprocess.run(["poe", "cmd", "authz", "migrate-existing-data"], check=True)
    subprocess.run(["poe", "cmd", "admin", "create-superuser"], check=True)
    print_success("------------------------------------------------------------")
    print_success(
        r"""
  ___ ___ _____ _   _ ___                 
 / __| __|_   _| | | | _ \                
 \__ \ _|  | | | |_| |  _/                
 |___/___| |_|  \___/|_|    ___ _____ ___ 
  / __/ _ \|  \/  | _ \ |  | __|_   _| __|
 | (_| (_) | |\/| |  _/ |__| _|  | | | _| 
  \___\___/|_|  |_|_| |____|___| |_| |___|

"""
    )
    print_success("------------------------------------------------------------")


if __name__ == "__main__":
    app()
