import os

from datasets import load_dataset, list_datasets
from .dataset import Dataset
from api.task_type import TaskType
from .dataset_dir import DatasetDir


class FillMaskDatasets:
    def __init__(self):
        self._datasets = self.__init_datasets()

    def get_datasets(self):
        return self._datasets

    @staticmethod
    def __init_datasets():
        all_datasets = list_datasets(with_community_datasets=True, with_details=True)
        fill_mask_datasets = dict()

        # TODO : jak przeflitrowac uzyskane zbiory danych po kategorii zadania

        # Narazie nie wiem jak przefiltrować zbiory uzyskane z bilbioteki datasets po kategorii zadania.
        # Narazie nazwy są ustawione na sztywno.

        datasets_name = [
            'numer_sense',
            'kilt_tasks'
        ]

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
