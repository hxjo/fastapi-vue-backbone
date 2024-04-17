import typer
import urllib.request
import os

from .admin import i as admin
from .authz import i as authz
from .docker import i as docker
from .options import Option, handle_options
from app.core.config import settings

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))

def update_openapi():
    # Url to fetch:
    typer.echo("Updating OpenAPI docs...")

    req = urllib.request.Request(f"{settings.SERVER_HOST}/api/openapi.json")
    with urllib.request.urlopen(req) as response:
        openapi = response.read()
        output_path = os.path.join(ABSOLUTE_PATH, "..", "..", "openapi.json")
        with open(output_path, "wb") as f:
            f.write(openapi)

    typer.echo("Done!")

def i():
    common_func_args = {"allow_back": True}
    handle_options(
        [
            Option(
                index=1,
                description="Docker commands 🐳",
                func=docker,
                func_args=common_func_args,
            ),
            Option(
                index=2,
                description="Admin commands 🪄",
                func=admin,
                func_args=common_func_args,
            ),
            Option(
                index=3,
                description="Authorization commands 🔑",
                func=authz,
                func_args=common_func_args,
            ),
            Option(
                index=4,
                description="Update OpenAPI docs",
                func=update_openapi,
            )
        ],
        allow_back=False,
    )


if __name__ == "__main__":
    typer.run(i)
