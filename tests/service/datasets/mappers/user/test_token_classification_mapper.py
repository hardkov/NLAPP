import json
import unittest

from nlapp.data_model.dataset_format import DatasetFormat
from nlapp.service.datasets.mappers.user.token_classification_mapper import (
    TokenClassificationMapper,
)
from tests.utils import get_resource_path


class TestTokenClassificationMapper(unittest.TestCase):
    def test_parse_json(self):
        # given
        mapping_columns = {
            "tokens": "token_classification.words",
            "ner_tags": "token_classification.results",
            "tag_names": "tags_mapping",
        }
        mapper = TokenClassificationMapper(mapping_columns, DatasetFormat.JSON)
        path = get_resource_path("token_classification_1.json")

        with open(path, "r") as f:
            dataset = json.load(f)

        # when
        mapped_dataset = mapper.map(dataset, DatasetFormat.JSON)
        chunks = mapped_dataset.get("chunks")

        # then
        self.assertTrue(len(chunks) == 2)
