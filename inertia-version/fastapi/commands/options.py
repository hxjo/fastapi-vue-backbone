from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

import typer
from rich.prompt import Prompt

from .print import print_default, print_info


@dataclass
class Option:
    index: int
    description: str
    func: Callable[..., Any]
    func_args: Optional[Dict[str, Any]] = None


def handle_options(options: List[Option], allow_back: bool) -> None:
    while True:
        print_info("What do you want to do ? 🤔")
        allowed_choices = []
        for option in options:
            allowed_choices.append(str(option.index))
            print_default(f"{option.index}. {option.description}")

        if allow_back:
            allowed_choices.append("0")
            print_default("0. Go back 🏠")

        allowed_choices.append("00")
        print_default("00. Exit 🚪")

        choice = Prompt.ask("Enter your choice", choices=allowed_choices)
        if choice == "00":
            print_default("Goodbye ! 👋")
            raise typer.Exit()

        if choice == "0":
            break

        for option in options:
            if choice == str(option.index):
                if option.func_args:
                    option.func(**option.func_args)
                else:
                    option.func()
                break
