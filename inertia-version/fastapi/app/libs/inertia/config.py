import os
from typing import Literal, Type
from json import JSONEncoder
from .utils import InertiaJsonEncoder
from dataclasses import dataclass

manifest_json_path = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "..", "vue", "dist", "client", "manifest.json"
)


@dataclass
class InertiaConfig:
    environment: Literal["development", "production"] = "development"
    version: str = "1.0"
    json_encoder: Type[JSONEncoder] = InertiaJsonEncoder
    manifest_json_path: str = manifest_json_path
    dev_url: str = "http://localhost:5173"
    ssr_url: str = "http://localhost:13714"
    ssr_enabled: bool = True
    use_typescript: bool = True
