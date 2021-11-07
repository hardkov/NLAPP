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

    def test_map_user_dataset_when_use_fill_mask_and_json(self):
        # given
        mapping_columns = {
            "sentence": "fillmask.phrase",
            "target": "fillmask.expected",
        }
        test_dir = dirname(dirname(dirname(abspath(__file__))))
        path = test_dir + "/_resources/fill_mask_1.json"

        with open(path, "r") as f:
            dataset = json.load(f)

        # when
        mapped_dataset = map_user_dataset(
            TaskType.FILL_MASK, mapping_columns, DatasetFormat.JSON, dataset
        )
        sentences = mapped_dataset.get("sentence")
        targets = mapped_dataset.get("target")

        # then
        self.assertTrue(len(sentences) == 3)
        self.assertTrue(len(targets) == 3)

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

    def test_map_user_dataset_when_use_question_answering_and_json(self):
        # given
        mapping_columns = {
            "context": "questionAnswer.text",
            "question": "questionAnswer.question",
            "answers": "questionAnswer.answer",
        }
        test_dir = dirname(dirname(dirname(abspath(__file__))))
        path = test_dir + "/_resources/question_answer_1.json"

        with open(path, "r") as f:
            dataset = json.load(f)

        # when
        mapped_dataset = map_user_dataset(
            TaskType.QUESTION_ANSWERING,
            mapping_columns,
            DatasetFormat.JSON,
            dataset,
        )
        contexts = mapped_dataset.get("context")
        questions = mapped_dataset.get("question")
        answers = mapped_dataset.get("answers")

        # then
        self.assertTrue(len(contexts) == 2)
        self.assertTrue(len(questions) == 2)
        self.assertTrue(len(answers) == 2)

    def test_download_dataset_when_use_summarization(self):
        # given
        dataset_name = "billsum"
        task_type = TaskType.SUMMARIZATION

        # when
        dataset = download_dataset(task_type, dataset_name)
        texts = dataset.get("text")

        # then
        self.assertTrue(len(texts) > 0)

    def test_map_user_dataset_when_use_summarization_and_json(self):
        # given
        mapping_columns = {
            "text": "summarization.context",
        }
        test_dir = dirname(dirname(dirname(abspath(__file__))))
        path = test_dir + "/_resources/summarization_1.json"

        with open(path, "r") as f:
            dataset = json.load(f)

        # when
        mapped_dataset = map_user_dataset(
            TaskType.SUMMARIZATION,
            mapping_columns,
            DatasetFormat.JSON,
            dataset,
        )
        texts = mapped_dataset.get("text")
        # then
        self.assertTrue(len(texts) == 4)
