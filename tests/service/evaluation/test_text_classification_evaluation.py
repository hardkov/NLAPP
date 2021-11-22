import unittest

from nlapp.data_model.model_dto import ModelDTO
from nlapp.service.datasets.dataset_gateway import download_dataset
from nlapp.service.models.model_gateway import download_model
from nlapp.data_model.task_type import TaskType
from nlapp.service.evaluation.text_classification_evaluation import *


class TestTextClassificationEvaluation(unittest.TestCase):
    def test_evaluate(self):
        # given
        model_dto = ModelDTO(
            "cross-encoder/ms-marco-MiniLM-L-6-v2",
            "Description",
            TaskType.TEXT_CLASSIFICATION,
            False,
        )
        model, tokenizer = download_model(model_dto)
        sentence = "I love Cracow"

        # when
        result = evaluate(sentence, model, tokenizer)

        # then
        self.assertTrue(len(result) > 0)
        self.assertTrue(result[0].score > 0.0)

    def test_evaluate_dataset(self):
        # given
        dataset_name = "ag_news"
        task_type = TaskType.TEXT_CLASSIFICATION
        model_dto = ModelDTO(
            "distilbert-base-uncased-finetuned-sst-2-english",
            "Description",
            task_type,
            False,
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
