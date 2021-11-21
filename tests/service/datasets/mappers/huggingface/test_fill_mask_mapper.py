import unittest

from datasets import load_dataset

from nlapp.service.datasets.dataset_tool import DATASET_DIR
from nlapp.service.datasets.mappers.huggingface.fill_mask_mapper import (
    FillMaskMapper,
)


class TestFillMaskMapper(unittest.TestCase):
    def test_parse_dataset_from_hugging_face(self):
        # given
        dataset_name = "numer_sense"
        dataset = load_dataset(dataset_name, cache_dir=DATASET_DIR)
        mapper = FillMaskMapper()

        # when
        mapped_dataset = mapper.map(dataset, dataset_name)
        sentences = mapped_dataset.get("sentence")
        targets = mapped_dataset.get("target")

        # then
        self.assertTrue(len(sentences) > 0)
        self.assertTrue(len(targets) > 0)
        self.assertTrue(len(sentences) == len(targets))
