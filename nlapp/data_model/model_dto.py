from dataclasses import dataclass

from nlapp.data_model import task_type


@dataclass
class ModelDTO:
    name: str
    description: any
    task_type: task_type
    cached: bool = False
