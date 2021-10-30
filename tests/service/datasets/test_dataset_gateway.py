import json
import unittest
from os.path import dirname, abspath

from nlapp.service.datasets.dataset_gateway import *


class TestDatasetGateway(unittest.TestCase):
    def test_download_dataset_when_use_fill_mask(self):
        # given
        dataset_name = "numer_sense"
        task_type = TaskType.FILL_MASK

        # when
        dataset = download_dataset(task_type, dataset_name)
        sentences = dataset.get("sentence")
        targets = dataset.get("target")

        # then
        self.assertTrue(len(sentences) > 0)
        self.assertTrue(len(targets) > 0)
        self.assertTrue(len(sentences) == len(targets))

    def test_map_user_dataset_when_use_fill_mask_and_json(self):
        # given
        mapping_columns = {
            "sentence": "fillmask.phrase",
            "target": "fillmask.expected",
        }
        test_dir = dirname(dirname(dirname(abspath(__file__))))
        path = test_dir + "/_resources/fill_mask_1.json"

        with open(path, "r") as f:
            dataset = json.load(f)

        # when
        mapped_dataset = map_user_dataset(
            TaskType.FILL_MASK, mapping_columns, DatasetFormat.JSON, dataset
        )
        sentences = mapped_dataset.get("sentence")
        targets = mapped_dataset.get("target")

        # then
        self.assertTrue(len(sentences) == 3)
        self.assertTrue(len(targets) == 3)
