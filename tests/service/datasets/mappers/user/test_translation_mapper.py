import json
import unittest

from nlapp.data_model.dataset_format import DatasetFormat
from nlapp.service.datasets.mappers.user.translation_mapper import TranslationMapper

from tests.utils import get_resource_path

class TestTranslationMapper(unittest.TestCase):
    def test_parse_json(self):
        # given
        mapping_columns = {
            "source": "translation.german",
            "targets": "translation.english",
        }
        mapper = TranslationMapper(mapping_columns)
        path = get_resource_path("translation_1.json")

        with open(path, "r") as f:
            dataset = json.load(f)

        # when
        mapped_dataset = mapper.map(dataset, DatasetFormat.JSON)
        source = mapped_dataset.get("source")
        targets = mapped_dataset.get("targets")

        # then
        self.assertTrue(len(source) == 3)
        self.assertTrue(len(targets) == 3)
