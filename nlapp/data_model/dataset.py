from dataclasses import dataclass
from nlapp.data_model.task_type import TaskType


@dataclass
class Dataset:
    name: str
    description: str
    task_type: TaskType
    cached: bool = False
