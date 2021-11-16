import unittest

from nlapp.data_model.dataset_format import DatasetFormat
from nlapp.service.datasets.mappers.user.fill_mask_mapper import FillMaskMapper


class TestFillMaskMapper(unittest.TestCase):
    def test_parse_json_when_contains_object(self):
        # given
        data_from_user = {
            "data": [
                {
                    "phrase": "Vistula is the biggest [MASK] in Poland.",
                    "expected": "river",
                },
                {
                    "phrase": "Coal is using to produce [MASK] energy.",
                    "expected": "electric",
                },
            ]
        }
        mapping_columns = {"sentence": "data.phrase", "target": "data.expected"}
        mapper = FillMaskMapper(mapping_columns)

        # when
        mapped_data = mapper.map(data_from_user, DatasetFormat.JSON)

        # then
        self.assertEqual(len(mapped_data.get("sentence")), 2)
        self.assertEqual(len(mapped_data.get("target")), 2)

    def test_parse_json_when_contains_array(self):
        # given
        data_from_user = {
            "phrase": [
                "Vistula is the biggest [MASK] in Poland.",
                "Coal is using to produce [MASK] energy.",
            ],
            "expected": ["river", "electric"],
        }
        mapping_columns = {"sentence": "phrase", "target": "expected"}
        mapper = FillMaskMapper(mapping_columns)

        # when
        mapped_data = mapper.map(data_from_user, DatasetFormat.JSON)

        # then
        self.assertEqual(
            mapped_data.get("sentence"), data_from_user.get("phrase")
        )
        self.assertEqual(
            mapped_data.get("target"), data_from_user.get("expected")
        )
