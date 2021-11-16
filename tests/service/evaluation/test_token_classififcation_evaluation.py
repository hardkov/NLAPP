import unittest

from nlapp.data_model.model_dto import ModelDTO
from nlapp.service.datasets.dataset_gateway import download_dataset
from nlapp.service.models.model_gateway import download_model
from nlapp.data_model.task_type import TaskType
from nlapp.service.evaluation.token_classification_evaluation import *


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
        dataset_name = "smartdata"
        task_type = TaskType.TOKEN_CLASSIFICATION
        model_dto = ModelDTO(
            "Emanuel/autonlp-pos-tag-bosque", "Description", task_type, False,
        )
        dataset = download_dataset(task_type, dataset_name)
        dataset = self.__limit_dataset(dataset)
        model, tokenizer = download_model(model_dto)

        # when
        result = evaluate_dataset(dataset, model, tokenizer)

        # then
        self.assertTrue(len(result.result_list) == 10)
        self.assertTrue(result.score_avg > 0.0)

    @staticmethod
    def __limit_dataset(dataset: Dict[str, List[str]], limit=10):
        keys = dataset.keys()
        for key in keys:
            dataset[key] = dataset.get(key)[0:limit]

        return dataset
