import unittest
from typing import Dict, List

from nlapp.data_model.model_dto import ModelDTO
from nlapp.data_model.task_type import TaskType
from nlapp.service.datasets.dataset_gateway import download_dataset
from nlapp.service.evaluation.summarization_evaluation import evaluate_dataset
from nlapp.service.evaluation.summarization_evaluation import evaluate
from nlapp.service.models.model_gateway import download_model


class TestSummarizationEvaluation(unittest.TestCase):
    def test_evaluate(self):
        # given
        model_dto = ModelDTO(
            "T-Systems-onsite/mt5-small-sum-de-en-v2",
            "Description",
            TaskType.SUMMARIZATION,
            False,
        )
        model, tokenizer = download_model(model_dto)
        text = (
            "London is the capital of England and the United Kingdom and one of the largest and most important "
            "cities in the world. The area was originally settled by early hunter gatherers around 6,000 B.C., "
            "and researchers have found evidence of Bronze Age bridges and Iron Age forts near the River "
            "Thames.Ancient Romans founded a port and trading settlement called Londinium in 43 A.D., "
            "and a few years later a bridge was constructed across the Thames to facilitate commerce and troop "
            "movements. But in 60 A.D., Celtic queen Boudicca led an army to sack the city, which was burned to "
            "the ground in the first of many fires to destroy London. "
        )

        # when
        result = evaluate(text, model, tokenizer)

        # then
        self.assertTrue(result.rouge_2_precision > 0.0)

    def test_evaluate_dataset(self):
        # given
        dataset_name = "billsum"
        task_type = TaskType.SUMMARIZATION
        model_dto = ModelDTO(
            "T-Systems-onsite/mt5-small-sum-de-en-v2",
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
        self.assertTrue(len(result.summaries) == 2)
        self.assertTrue(result.rouge_2_recall_avg > 0.0)
        self.assertTrue(result.rouge_2_precision_avg > 0.0)

    @staticmethod
    def __limit_dataset(dataset: Dict[str, List[str]], limit=2):
        keys = dataset.keys()
        for key in keys:
            dataset[key] = dataset.get(key)[0:limit]

        return dataset
