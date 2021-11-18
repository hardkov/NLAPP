import os
from enum import Enum
from pathlib import Path

from nlapp.data_model.model_dto import ModelDTO
from nlapp.data_model.task_type import TaskType

MODEL_DIR = os.path.join(
    Path(__file__).parent.parent.parent.parent.absolute(), "data", "models"
)


class ModelDir(Enum):
    FILL_MASK = (MODEL_DIR + "/fillMask",)
    QUESTION_ANSWERING = (MODEL_DIR + "/questionAnswering",)
    SUMMARIZATION = (MODEL_DIR + "/summarization",)
    TEXT_CLASSIFICATION = (MODEL_DIR + "/textClassification",)
    TOKEN_CLASSIFICATION = (MODEL_DIR + "/tokenClassification",)
    TRANSLATION = (MODEL_DIR + "/translation",)

    @staticmethod
    def from_task_type(task_type: TaskType):
        switcher = {
            TaskType.SUMMARIZATION: ModelDir.SUMMARIZATION,
            TaskType.FILL_MASK: ModelDir.FILL_MASK,
            TaskType.TRANSLATION: ModelDir.TRANSLATION,
            TaskType.TEXT_CLASSIFICATION: ModelDir.TEXT_CLASSIFICATION,
            TaskType.TOKEN_CLASSIFICATION: ModelDir.TOKEN_CLASSIFICATION,
            TaskType.QUESTION_ANSWERING: ModelDir.QUESTION_ANSWERING,
        }
        if task_type in switcher:
            return switcher[task_type].value[0]
        else:
            raise NotImplementedError

    @staticmethod
    def cache_dir(model: ModelDTO):
        model.cached = True
        return f"{ModelDir.from_task_type(model.task_type)}/{model.name}"

    @staticmethod
    def is_cached(name: str, task_type: TaskType):
        path = f"{ModelDir.from_task_type(task_type)}/{name}"
        return os.path.exists(path)
