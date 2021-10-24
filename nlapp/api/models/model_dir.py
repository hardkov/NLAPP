import os
from enum import Enum

from nlapp.api.models.model import Model
from nlapp.api.task_type import TaskType

MODEL_DIR = os.getcwd() + "/data/models"


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
    def cache_dir(model: Model):
        model.cached = True
        return f"{ModelDir.from_task_type(model.task_type)}/{model.name}"
