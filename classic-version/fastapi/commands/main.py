import typer

from .admin import i as admin
from .authz import i as authz
from .docker import i as docker
from .options import Option, handle_options
from .setup import setup


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
                index=99,
                description="First setup",
                func=setup,
            ),
        ],
        allow_back=False,
    )


if __name__ == "__main__":
    typer.run(i)
