import json
import os
import subprocess

import typer
from dotenv import load_dotenv
from openfga_sdk.models.create_store_request import CreateStoreRequest

from openfga_sdk import ClientConfiguration
from openfga_sdk.sync import OpenFgaClient

from app.core.config import settings

from .options import Option, handle_options
from .print import print_error, print_success

app = typer.Typer()

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(ABSOLUTE_PATH, "..", ".env")
AUTHORIZATION_FOLDER = os.path.join(ABSOLUTE_PATH, "..", "authorization")
FGA_AUTHZ_MODEL = os.path.join(AUTHORIZATION_FOLDER, "model.fga")
FGA_AUTHZ_STORE = os.path.join(AUTHORIZATION_FOLDER, "store.fga.yaml")
JSON_AUTHZ_MODEL = os.path.join(AUTHORIZATION_FOLDER, "model.json")

fga_client_configuration = ClientConfiguration(
    api_scheme=settings.FGA_API_SCHEME,
    api_host=f"{settings.FGA_API_HOST}:{settings.FGA_API_PORT}",
    store_id=settings.FGA_STORE_ID,
    authorization_model_id=settings.FGA_MODEL_ID,
)


def write_to_dotenv(key: str, value: str):
    key_exists = False
    try:
        with open(ENV_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for index, line in enumerate(lines):
                if line.startswith(key):
                    key_exists = True
                    lines[index] = f"{key}={value}\n"
                    break
    except FileNotFoundError:
        lines = []

    if not key_exists:
        lines.append(f"\n{key}={value}\n")

    with open(ENV_FILE, "w", encoding="utf-8") as file:
        file.writelines(lines)


@app.command()
def setup_store():
    with OpenFgaClient(fga_client_configuration) as client:
        create_store_request = CreateStoreRequest(
            name="skeleton",
        )
        response = client.create_store(create_store_request)
        print_success("Store created successfully")

        write_to_dotenv("FGA_STORE_ID", response.id)

        print_success("Your .env file has been updated")


@app.command()
def model_to_json():
    """
    Convert model to json
    """
    try:
        subprocess.run(["fga", "version"], check=True)
    except FileNotFoundError:
        print_error(
            "Please install fga cli. "
            + "[link=https://github.com/openfga/cli/?tab=readme-ov-file#installation]See documentation[/link]"
        )
        return

    try:
        command = subprocess.run(
            ["fga", "model", "transform", "--file", FGA_AUTHZ_MODEL],
            check=True,
            capture_output=True,
            text=True,
        )
        json_model = json.loads(command.stdout)
        with open(JSON_AUTHZ_MODEL, "w", encoding="utf-8") as file:
            file.write(json.dumps(json_model, indent=4))

        print_success("Model converted to json and saved in authorization/model.json")

    except subprocess.CalledProcessError:
        print_error("An error occurred while converting the model to json")
        return


@app.command()
def write_authorization_model():
    load_dotenv(override=True)
    store_id = os.getenv("FGA_STORE_ID")
    if store_id is None:
        print_error("Store ID is not set")
        return
    with open(JSON_AUTHZ_MODEL, "r", encoding="utf-8") as model:
        model_json = json.load(model)
        with OpenFgaClient(fga_client_configuration) as client:
            client.set_store_id(store_id)
            response = client.write_authorization_model(model_json)
            print_success("Authorization model written successfully")

            write_to_dotenv("FGA_MODEL_ID", response.authorization_model_id)

            print_success("Your .env file has been updated")


@app.command()
def setup():
    """
    Setup FGA store and write authorization model
    """
    setup_store()
    write_authorization_model()


@app.command()
def migrate_existing_data():
    """
    Migrate existing data
    """
    print_error("Not implemented yet")


@app.command()
def test_model():
    try:
        subprocess.run(["fga", "version"], check=True)
    except FileNotFoundError:
        print_error(
            "Please install fga cli."
            + "[link=https://github.com/openfga/cli/?tab=readme-ov-file#installation]See documentation[/link]"
        )
        return

    try:
        subprocess.run(
            ["fga", "model", "test", f"--tests={FGA_AUTHZ_STORE}"], check=True
        )
    except subprocess.CalledProcessError:
        print_error("An error occurred while testing the model")
        return


@app.command()
def update():
    model_to_json()
    write_authorization_model()


@app.command()
def i(allow_back: bool = False):
    """
    Interactive mode
    """
    handle_options(
        [
            Option(index=1, description="Setup FGA store", func=setup_store),
            Option(index=2, description="Convert model to json", func=model_to_json),
            Option(
                index=3,
                description="Write authorization model",
                func=write_authorization_model,
            ),
            Option(index=4, description="Setup", func=setup),
            Option(index=5, description="Test model", func=test_model),
            Option(
                index=6, description="Migrate existing data", func=migrate_existing_data
            ),
            Option(index=7, description="Update (json + write model)", func=update),
        ],
        allow_back=allow_back,
    )


if __name__ == "__main__":
    app()
