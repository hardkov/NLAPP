import unittest

from nlapp.data_model.model_dto import ModelDTO
from nlapp.service.datasets.dataset_gateway import download_dataset
from nlapp.service.models.model_gateway import download_model
from nlapp.data_model.task_type import TaskType
from nlapp.service.evaluation.translation_evaluation import *


class TestTranslationEvaluation(unittest.TestCase):
    def test_evaluate(self):
        # given
        model_dto = ModelDTO(
            "persiannlp/mt5-small-parsinlu-opus-translation_fa_en",
            "Description",
            TaskType.TRANSLATION,
            False,
        )
        model, tokenizer = download_model(model_dto)
        sentence = "ستایش خدای را که پروردگار جهانیان است."

        # when
        result = evaluate(sentence, model, tokenizer)

        # then
        self.assertTrue(len(result.translation) > 0)

    def test_evaluate_dataset(self):
        # given
        dataset_name = "persiannlp/parsinlu_translation_fa_en"
        task_type = TaskType.TRANSLATION
        model_dto = ModelDTO(
            "persiannlp/mt5-small-parsinlu-opus-translation_fa_en", "Description", task_type, False,
        )
        dataset = download_dataset(task_type, dataset_name)
        dataset = self.__limit_dataset(dataset)
        model, tokenizer = download_model(model_dto)

        # when
        result = evaluate_dataset(dataset, model, tokenizer)

        # then
        self.assertTrue(len(result.translations_scores) == 10)
        self.assertTrue(result.bleu_avg > 0.0)

    @staticmethod
    def __limit_dataset(dataset: Dict[str, List[str]], limit=10):
        keys = dataset.keys()
        for key in keys:
            dataset[key] = dataset.get(key)[0:limit]

        return dataset
