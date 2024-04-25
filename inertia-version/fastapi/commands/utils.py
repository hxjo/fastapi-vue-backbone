import os
import importlib


def import_all_models() -> None:
    # Define the path to the modules directory
    modules_path = os.path.join("app", "modules")

    # List all subdirectories in the modules directory
    module_folders = [f.name for f in os.scandir(modules_path) if f.is_dir()]
    importlib.import_module("app.user.models")
    importlib.import_module("app.auth.models")

    # Import models from each module
    for folder in module_folders:
        try:
            # Dynamically import the models.py file from each folder
            importlib.import_module(f"app.modules.{folder}.models")

        except ModuleNotFoundError:
            pass
