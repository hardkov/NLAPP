import json
import unittest

from nlapp.data_model.dataset_format import DatasetFormat
from nlapp.service.datasets.mappers.user.question_answering_mapper import QuestionAnsweringMapper
from tests.utils import get_resource_path


class TestQuestionAnsweringMapper(unittest.TestCase):

    def test_parse_json(self):
        # given
        mapping_columns = {
            "context": "questionAnswer.text",
            "question": "questionAnswer.question",
            "answers": "questionAnswer.answer",
        }
        mapper = QuestionAnsweringMapper(mapping_columns)
        path = get_resource_path("question_answer_1.json")

        with open(path, "r") as f:
            dataset = json.load(f)

        # when
        mapped_dataset = mapper.map(dataset, DatasetFormat.JSON)

        # then
        self.assert_data(mapped_dataset)

    def test_parse_conll(self):
        # given
        mapping_columns = {
            "context": "text",
            "question": "question",
            "answers": "expectation",
        }
        mapper = QuestionAnsweringMapper(mapping_columns)
        path = get_resource_path("question_answer_1.conllu")

        with open(path, "r") as f:
            dataset = f.read()

        # when
        mapped_dataset = mapper.map_conll(dataset)

        # then
        self.assert_data(mapped_dataset)

    def assert_data(self, mapped_dataset):
        contexts = mapped_dataset.get("context")
        questions = mapped_dataset.get("question")
        answers = mapped_dataset.get("answers")
        self.assertTrue(len(contexts) == 2)
        self.assertTrue(len(questions) == 2)
        self.assertTrue(len(answers) == 2)



