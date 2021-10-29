from dataclasses import dataclass
from nlapp.data_model.task_type import TaskType


@dataclass
class DatasetDTO:
    name: str
    description: str
    task_type: TaskType
    cached: bool = False
