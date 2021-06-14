import os
import csv

from datasets import load_dataset, list_datasets
from .dataset import Dataset
from api.task_type import TaskType
from .dataset_dir import DatasetDir


class FillMaskDatasets:
    def __init__(self):
        self.csv_file = os.getcwd() + '/api/data/datasets.csv'
        self._datasets = self.__init_datasets()

    def get_datasets(self):
        return self._datasets

    def __init_datasets(self):
        all_datasets = list_datasets(with_community_datasets=True, with_details=True)
        datasets_name = self.read_datasets_name()
        fill_mask_datasets = dict()

        for dataset in all_datasets:
            if dataset.id in datasets_name:
                fill_mask_datasets[dataset.id] = Dataset(dataset.id, dataset.description, TaskType.FILL_MASK)

        return fill_mask_datasets

    def download_dataset(self, name):
        if self._datasets[name] is None:
            raise Exception("Dataset name is incorrect.")

        self.create_dir()
        self._datasets[name].cached = True

        # TODO : czasami jeden zbiór może być do kilku zadań, to wtedy pasowałoby go sciągnąć tylko raz
        return load_dataset(name, cache_dir=DatasetDir.FILL_MASK.value)

    @staticmethod
    def create_dir():
        if not os.path.exists(DatasetDir.FILL_MASK.value):
            os.makedirs(DatasetDir.FILL_MASK.value)

    def read_datasets_name(self):
        with open(self.csv_file, 'r+') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == TaskType.FILL_MASK.name:
                    return row[1]
