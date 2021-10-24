from dataclasses import dataclass

from nlapp.api import task_type


@dataclass
class Model:
    name: str
    description: any
    task_type: task_type
    cached: bool = False
