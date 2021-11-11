import unittest

from datasets import load_dataset

from nlapp.service.datasets.dataset_tool import DATASET_DIR
from nlapp.service.datasets.mappers.huggingface.token_classification_mapper import (
    TokenClassificationMapper,
)


class TestFillMaskMapper(unittest.TestCase):
    def test_parse_dataset_from_hugging_face(self):
        # given
        dataset_name = "harem"
        dataset = load_dataset(dataset_name, cache_dir=DATASET_DIR)
        mapper = TokenClassificationMapper()

        # when
        mapped_dataset = mapper.map(dataset)
        tokens = mapped_dataset.get("tokens")
        ner_tags = mapped_dataset.get("ner_tags")

        # then
        self.assertTrue(len(tokens) > 0)
        self.assertTrue(len(ner_tags) > 0)
        self.assertTrue(len(tokens) == len(ner_tags))
