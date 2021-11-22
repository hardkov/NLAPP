import unittest

from nlapp.data_model.model_dto import ModelDTO
from nlapp.data_model.task_type import TaskType
from nlapp.data_model.token_classification.chunk import Chunk
from nlapp.service.evaluation.token_classification_evaluation import *
from nlapp.service.models.model_gateway import download_model


class TestTokenClassificationEvaluation(unittest.TestCase):
    def test_evaluate(self):
        # given
        model_dto = ModelDTO(
            "Emanuel/autonlp-pos-tag-bosque",
            "Description",
            TaskType.TOKEN_CLASSIFICATION,
            False,
        )
        model, tokenizer = download_model(model_dto)
        sentence = "My name is Clara and I live in Berkeley, California."

        # when
        result = evaluate(sentence, model, tokenizer)

        # then
        self.assertTrue(len(result) > 0)

    def test_evaluate_dataset(self):
        # given
        task_type = TaskType.TOKEN_CLASSIFICATION
        model_dto = ModelDTO(
            "Emanuel/autonlp-pos-tag-bosque",
            "Description",
            task_type,
            False,
        )

        chunk1 = Chunk(
            "Peter Blackburn", [("Peter", "B-NP"), ("Blackburn", "I-NP")]
        )
        chunk2 = Chunk(
            "China says time right for Taiwan talks",
            [
                ("China", "B-NP"),
                ("says", "B-VP"),
                ("time", "B-NP"),
                ("right", "B-VP"),
                ("for", "B-NP"),
                ("Taiwan", "B-PP"),
                ("talks", "B-VP"),
            ],
        )

        dataset = {"chunks": [chunk1, chunk2]}
        model, tokenizer = download_model(model_dto)

        # when
        result = evaluate_dataset(dataset, model, tokenizer)

        # then
        self.assertTrue(len(result.wrong_predictions) <= 2)
        self.assertTrue(len(result.correct_predictions) <= 2)
        self.assertTrue(result.score_avg > 0.0)
