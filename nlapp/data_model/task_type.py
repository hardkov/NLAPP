from enum import Enum

from transformers import (
    AutoModelForMaskedLM,
    AutoModelForQuestionAnswering,
    AutoModelForSequenceClassification,
    AutoModelForSeq2SeqLM,

)


class TaskType(Enum):
    FILL_MASK = 1
    QUESTION_ANSWERING = 2
    SUMMARIZATION = 3
    TEXT_CLASSIFICATION = 4
    TOKEN_CLASSIFICATION = 5
    TRANSLATION = 6

    @staticmethod
    def from_str(label):
        switcher = {
            "fill-mask": TaskType.FILL_MASK,
            "question-answering": TaskType.QUESTION_ANSWERING,
            "summarization": TaskType.SUMMARIZATION,
            "text-classification": TaskType.TEXT_CLASSIFICATION,
            "token-classification": TaskType.TOKEN_CLASSIFICATION,
            "translation": TaskType.TRANSLATION,
        }
        if label in switcher:
            return switcher[label]
        else:
            raise NotImplementedError

    def get_dataset_filter(self):
        filters = {
            TaskType.FILL_MASK: "task_ids:slot-filling",
            TaskType.QUESTION_ANSWERING: "task_categories:question-answering",
            TaskType.SUMMARIZATION: "task_ids:summarization",
            TaskType.TEXT_CLASSIFICATION: "task_categories:text-classification",
            TaskType.TOKEN_CLASSIFICATION: "task_ids:named-entity-recognition",
            TaskType.TRANSLATION: "task_categories:translation",
        }

        return filters[self]

    def get_model_filter(self):
        filters = {
            TaskType.FILL_MASK: "fill-mask",
            TaskType.QUESTION_ANSWERING: "question-answering",
            TaskType.SUMMARIZATION: "summarization",
            TaskType.TEXT_CLASSIFICATION: "text-classification",
            TaskType.TOKEN_CLASSIFICATION: "token-classification",
            TaskType.TRANSLATION: "translation",
        }

        return filters[self]

    def get_model_generator(self):
        generators = {
            TaskType.FILL_MASK: AutoModelForMaskedLM,
            TaskType.QUESTION_ANSWERING: AutoModelForQuestionAnswering,
            TaskType.TEXT_CLASSIFICATION: AutoModelForSequenceClassification,
            TaskType.SUMMARIZATION: AutoModelForSeq2SeqLM,
        }

        return generators[self]
