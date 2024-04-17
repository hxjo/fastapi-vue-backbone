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

AUTHORIZATION_MODEL_ID_FILE = os.path.join(ABSOLUTE_PATH, '..', 'app', '.fga_authorization_model_id')
STORE_ID_FILE = os.path.join(ABSOLUTE_PATH, '..', 'app', '.fga_store_id')



def get_fga_client_config():
    if not os.path.isfile(AUTHORIZATION_MODEL_ID_FILE):
        with open(AUTHORIZATION_MODEL_ID_FILE, "w", encoding="utf-8") as file:
            file.write("")
    if not os.path.isfile(STORE_ID_FILE):
        with open(STORE_ID_FILE, "w", encoding="utf-8") as file:
            file.write("")

    authorization_model_id =  open(AUTHORIZATION_MODEL_ID_FILE).read().strip()
    store_id = open(STORE_ID_FILE).read().strip()

    return ClientConfiguration(
        api_scheme=settings.FGA_API_SCHEME,
        api_host=f"{settings.FGA_API_HOST}:{settings.FGA_API_PORT}",
        store_id=store_id,
        authorization_model_id=authorization_model_id,
    )




@app.command()
def setup_store():
    config = get_fga_client_config()
    with OpenFgaClient(config) as client:
        create_store_request = CreateStoreRequest(
            name="skeleton",
        )
        response = client.create_store(create_store_request)
        print_success("Store created successfully")
        with open(STORE_ID_FILE, "w", encoding="utf-8") as file:
            file.write(response.id)
        print_success("Your store_id file has been updated")


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
    with open(STORE_ID_FILE, "r", encoding="utf-8") as file:
        store_id = file.read().strip()
    if store_id == "":
        print_error("Store ID is not set")
        return
    with open(JSON_AUTHZ_MODEL, "r", encoding="utf-8") as model:
        model_json = json.load(model)
        config = get_fga_client_config()
        with OpenFgaClient(config) as client:
            client.set_store_id(store_id)
            response = client.write_authorization_model(model_json)
            print_success("Authorization model written successfully")
            with open(AUTHORIZATION_MODEL_ID_FILE, "w", encoding="utf-8") as file:
                file.write(response.authorization_model_id)
                
            print_success("Your authorization file has been updated")



def is_first_time():
    config = get_fga_client_config()
    with OpenFgaClient(config) as client:
        existing_stores_res = client.list_stores()
        return len(existing_stores_res.stores) == 0

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
