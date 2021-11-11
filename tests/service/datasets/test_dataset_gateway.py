import json
import unittest
from os.path import dirname, abspath

from nlapp.service.datasets.dataset_gateway import *


class TestDatasetGateway(unittest.TestCase):
    def test_download_dataset_when_use_fill_mask(self):
        # given
        dataset_name = "numer_sense"
        task_type = TaskType.FILL_MASK

        # when
        dataset = download_dataset(task_type, dataset_name)
        sentences = dataset.get("sentence")
        targets = dataset.get("target")

        # then
        self.assertTrue(len(sentences) > 0)
        self.assertTrue(len(targets) > 0)
        self.assertTrue(len(sentences) == len(targets))

    def test_download_dataset_when_use_question_answering(self):
        # given
        dataset_name = "squad"
        task_type = TaskType.QUESTION_ANSWERING

        # when
        dataset = download_dataset(task_type, dataset_name)
        contexts = dataset.get("context")
        questions = dataset.get("question")
        answers = dataset.get("answers")

        # then
        self.assertTrue(len(contexts) == len(questions) == len(answers))

    def test_download_dataset_when_use_summarization(self):
        # given
        dataset_name = "billsum"
        task_type = TaskType.SUMMARIZATION

        # when
        dataset = download_dataset(task_type, dataset_name)
        texts = dataset.get("text")

        # then
        self.assertTrue(len(texts) > 0)
