from abc import ABC
from abc import abstractmethod
from typing import Dict

from datasets.dataset_dict import DatasetDict


class DatasetMapper(ABC):
    @abstractmethod
    def map(self, dataset: DatasetDict) -> Dict[str, list[str]]:
        pass

    @abstractmethod
    def is_correct(self, dataset: DatasetDict, dataset_name: str) -> bool:
        pass
