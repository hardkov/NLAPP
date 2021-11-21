import unittest

from nlapp.data_model.task_type import TaskType
from nlapp.service.datasets.dataset_gateway import (
    download_dataset,
    get_datasets_by_task_type,
)


class TestTokenClassification(unittest.TestCase):
    def test_parse_dataset_from_hugging_face(self):
        # given
        dataset_name = "harem"
        get_datasets_by_task_type(TaskType.TOKEN_CLASSIFICATION)

        # when
        mapped_dataset = download_dataset(
            TaskType.TOKEN_CLASSIFICATION, dataset_name
        )
        chunks = mapped_dataset.get("chunks")

        # then
        self.assertTrue(len(chunks) > 0)
