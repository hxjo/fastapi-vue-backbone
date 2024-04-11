from rich.console import Console
from rich.style import Style

console = Console()
danger_style = Style(color="red", blink=True, bold=True)
success_style = Style(color="green", bold=True)
warning_style = Style(color="yellow", bold=True)
info_style = Style(color="blue", bold=True)


def print_default(message: str) -> None:
    console.print(f"{message}")


def print_info(message: str) -> None:
    console.print(f"{message}", style=info_style)


def print_success(message: str) -> None:
    console.print(f"{message}", style=success_style)


def print_error(message: str) -> None:
    console.print(f"{message}", style=danger_style)


def print_warning(message: str) -> None:
    console.print(f"{message}", style=warning_style)
