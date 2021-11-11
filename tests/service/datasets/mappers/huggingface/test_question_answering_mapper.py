import unittest

from datasets import load_dataset

from nlapp.service.datasets.dataset_tool import DATASET_DIR
from nlapp.service.datasets.mappers.huggingface.question_answering_mapper import QuestionAnsweringMapper


class TestQuestionAnsweringMapper(unittest.TestCase):

    def test_parse_dataset_from_hugging_face(self):
        # given
        dataset_name = "squad"
        dataset = load_dataset(dataset_name, cache_dir=DATASET_DIR)
        mapper = QuestionAnsweringMapper()

        # when
        mapped_dataset = mapper.map(dataset)
        contexts = mapped_dataset.get("context")
        questions = mapped_dataset.get("question")
        answers = mapped_dataset.get("answers")

        # then
        self.assertTrue(len(contexts) == len(questions) == len(answers))
