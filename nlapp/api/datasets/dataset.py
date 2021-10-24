from dataclasses import dataclass
from nlapp.api.task_type import TaskType


@dataclass
class Dataset:
    name: str
    description: str
    task_type: TaskType
    cached: bool = False
