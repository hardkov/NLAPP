import os
from pathlib import Path

RESOURCE_DIR = os.path.join(
    Path(__file__).parent.absolute(),
    "_resources",
)


def get_resource_path(file: str):
    return os.path.join(RESOURCE_DIR, file)
