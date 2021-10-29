from abc import ABC
from abc import abstractmethod
from typing import Dict

from nlapp.data_model.dataset_format import DatasetFormat


class UserDatasetMapper(ABC):
    def __init__(self, columns: list[str], column_mapping: Dict[str, str]):
        self.columns = columns
        self.column_mapping = column_mapping
        if self.validate_mapping() is False:
            raise Exception("Incorrect mapping.")

    def validate_mapping(self) -> bool:
        for column in self.columns:
            if self.column_mapping.get(column) is None:
                return False
        return True

    def map(self, data: dict, file_type: DatasetFormat) -> Dict[str, list[str]]:
        return {DatasetFormat.JSON: self.map_json(data)}.get(file_type)

    @abstractmethod
    def map_json(self, data):
        pass

    # TODO: add another format in future, now just prepare json format + dataset from huggingFace
