from enum import Enum

from transformers import (
    AutoModelForMaskedLM,
    AutoModelForQuestionAnswering,
    AutoModelForSequenceClassification,
    AutoModelForSeq2SeqLM,
    AutoModelForTokenClassification,
)


FILL_MASK_DESCRIPTION = (
    "Filling missing words in the given sentence the most probable choice of words. "
    "They are marked with special token: [MASK]."
)
QUESTION_ANSWERING_DESCRIPTION = (
    "Extracting (without rewording or creating) an answer to a given "
    "question, from a given context"
)

SUMMARIZATION_DESCRIPTION = (
    "Shortening long pieces of text. The intention is to create a coherent "
    "and fluent summary having only the main points outlined in the document."
)

TEXT_CLASSIFICATION_DESCRIPTION = (
    "Assigning a certain predefined categories to a given text. The most "
    "popular variants are: sentiment analysis, topic labeling, spam detection, "
    "intent detection."
)

TOKEN_CLASSIFICATION_DESCRIPTION = (
    "Breaking down a piece of text into small units called tokens. A token "
    "may be a word, part of a word or just characters like punctuation."
)

TRANSLATION_DESCRIPTION = (
    "Converting a given text from one language to the other. "
    "The languages used depend on the chosen model"
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
            TaskType.TOKEN_CLASSIFICATION: AutoModelForTokenClassification,
            TaskType.TRANSLATION: AutoModelForSeq2SeqLM,
        }

        return generators[self]

    def display_name(self) -> str:
        names = {
            TaskType.FILL_MASK: "Fill-Mask",
            TaskType.QUESTION_ANSWERING: "Question Answering",
            TaskType.TEXT_CLASSIFICATION: "Text Classification",
            TaskType.SUMMARIZATION: "Summarization",
            TaskType.TOKEN_CLASSIFICATION: "Token Classification",
            TaskType.TRANSLATION: "Translation",
        }

        return names[self]

    def description(self):
        tasks_descriptions = {
            TaskType.FILL_MASK: FILL_MASK_DESCRIPTION,
            TaskType.QUESTION_ANSWERING: QUESTION_ANSWERING_DESCRIPTION,
            TaskType.SUMMARIZATION: SUMMARIZATION_DESCRIPTION,
            TaskType.TEXT_CLASSIFICATION: TEXT_CLASSIFICATION_DESCRIPTION,
            TaskType.TOKEN_CLASSIFICATION: TOKEN_CLASSIFICATION_DESCRIPTION,
            TaskType.TRANSLATION: TRANSLATION_DESCRIPTION,
        }

        return tasks_descriptions[self]
