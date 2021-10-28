from abc import ABC
from abc import abstractmethod
from datasets.dataset_dict import DatasetDict


class DatasetMapper(ABC):

    @abstractmethod
    def map(self, dataset: DatasetDict) -> dict[str, list[str]]:
        pass

    @abstractmethod
    def is_correct(self, dataset: DatasetDict) -> bool:
        pass
