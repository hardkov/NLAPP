import json
import unittest

from nlapp.data_model.dataset_format import DatasetFormat
from nlapp.service.datasets.mappers.user.summarization_mapper import SummarizationMapper
from tests.utils import get_resource_path


class TestSummarizationMapper(unittest.TestCase):

    def test_parse_json(self):
        # given
        mapping_columns = {
            "text": "summarization.context",
        }
        mapper = SummarizationMapper(mapping_columns)
        path = get_resource_path("summarization_1.json")

        with open(path, "r") as f:
            dataset = json.load(f)

        mapped_data = mapper.map(dataset, DatasetFormat.JSON)
        texts = mapped_data.get("text")
        # then
        self.assertTrue(len(texts) == 4)
