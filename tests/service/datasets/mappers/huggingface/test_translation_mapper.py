import unittest

from datasets import load_dataset

from nlapp.service.datasets.dataset_tool import DATASET_DIR
from nlapp.service.datasets.mappers.huggingface.translation_mapper import (
    TranslationMapper,
)


class TestFillMaskMapper(unittest.TestCase):
    def test_parse_dataset_from_hugging_face(self):
        # given
        dataset_name = "persiannlp/parsinlu_translation_en_fa"
        dataset = load_dataset(dataset_name, cache_dir=DATASET_DIR)
        mapper = TranslationMapper()

        # when
        mapped_dataset = mapper.map(dataset)
        source = mapped_dataset.get("source")
        targets = mapped_dataset.get("targets")

        # then
        self.assertTrue(len(source) > 0)
        self.assertTrue(len(targets) > 0)
        self.assertTrue(len(source) == len(targets))
