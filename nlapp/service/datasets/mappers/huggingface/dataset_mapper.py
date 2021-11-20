from abc import ABC
from abc import abstractmethod
from typing import Dict, List

from datasets.dataset_dict import DatasetDict


class DatasetMapper(ABC):
    @abstractmethod
    def map(self, dataset: DatasetDict, dataset_name: str) -> Dict[str, List]:
        pass

    @abstractmethod
    def is_correct(self, dataset: Dict, dataset_name: str) -> bool:
        pass
