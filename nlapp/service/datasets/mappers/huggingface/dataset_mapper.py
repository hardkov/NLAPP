from abc import ABC
from abc import abstractmethod
from typing import Dict, List

from datasets.dataset_dict import DatasetDict


class DatasetMapper(ABC):
    @abstractmethod
    def map(self, dataset: DatasetDict) -> Dict[str, List[str]]:
        pass

    @abstractmethod
    def is_correct(self, dataset: Dict, dataset_name: str) -> bool:
        pass
