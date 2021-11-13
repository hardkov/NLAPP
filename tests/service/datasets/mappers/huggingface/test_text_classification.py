import unittest

from datasets import load_dataset

from nlapp.service.datasets.dataset_tool import DATASET_DIR
from nlapp.service.datasets.mappers.huggingface.text_classification_mapper import (
    TextClassificationMapper,
)


class TestFillMaskMapper(unittest.TestCase):
    def test_parse_dataset_from_hugging_face(self):
        # given
        dataset_name = "ag_news"
        dataset = load_dataset(dataset_name, cache_dir=DATASET_DIR)
        mapper = TextClassificationMapper()

        # when
        mapped_dataset = mapper.map(dataset)
        text = mapped_dataset.get("text")
        label = mapped_dataset.get("label")

        # then
        self.assertTrue(len(text) > 0)
        self.assertTrue(len(label) > 0)
        self.assertTrue(len(text) == len(label))
