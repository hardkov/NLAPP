import unittest

from datasets import load_dataset

from nlapp.service.datasets.dataset_tool import DATASET_DIR
from nlapp.service.datasets.mappers.huggingface.summarization_mapper import (
    SummarizationMapper,
)


class TestSummarizationMapper(unittest.TestCase):
    def test_parse_dataset_from_hugging_face(self):
        # given
        dataset_name = "billsum"
        data = load_dataset(dataset_name, cache_dir=DATASET_DIR)
        mapper = SummarizationMapper()

        # when
        mapped_dataset = mapper.map(data, dataset_name)
        texts = mapped_dataset.get("text")

        # then
        self.assertTrue(len(texts) > 0)
