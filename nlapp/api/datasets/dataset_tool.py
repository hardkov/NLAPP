import os
import csv
from pathlib import Path

from datasets import load_dataset, list_datasets
from .dataset import Dataset
from nlapp.api.task_type import TaskType


class DatasetTool:
    def __init__(self, task_type: TaskType):
        self.task_type = task_type
        self.cached_dir = os.path.join(
            Path(__file__).parent.parent.parent.absolute(), "data", "datasets"
        )
        self.csv_file = os.path.join(
            Path(__file__).parent.parent.absolute(), "data", "datasets.csv"
        )
        self._datasets = self.__init_datasets()

    def get_datasets(self):
        return self._datasets

    def __init_datasets(self):
        all_datasets = list_datasets(
            with_community_datasets=True, with_details=True
        )
        datasets_name = self.read_datasets_name()
        fill_mask_datasets = dict()

        for dataset in all_datasets:
            if dataset.id in datasets_name:
                fill_mask_datasets[dataset.id] = Dataset(
                    dataset.id, dataset.description, self.task_type
                )

        return fill_mask_datasets

    def download_dataset(self, name):
        if self._datasets[name] is None:
            raise Exception("Dataset name is incorrect.")

        self.create_dir()
        self._datasets[name].cached = True

        return load_dataset(name, cache_dir=self.cached_dir)

    def create_dir(self):
        if not os.path.exists(self.cached_dir):
            os.makedirs(self.cached_dir)

    def read_datasets_name(self):
        with open(self.csv_file, "r+") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == self.task_type.name:
                    return row[1]
