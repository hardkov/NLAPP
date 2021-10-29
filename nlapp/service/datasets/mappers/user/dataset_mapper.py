from abc import ABC
from abc import abstractmethod

from nlapp.data_model.dataset_format import DatasetFormat


class UserDatasetMapper(ABC):
    def __init__(self, columns: list[str], column_mapping: dict[str, str]):
        self.columns = columns
        self.column_mapping = column_mapping
        if self.validate_mapping() is False:
            raise Exception("Incorrect mapping.")

    def validate_mapping(self) -> bool:
        for column in self.columns:
            if self.column_mapping.get(column) is None:
                return False
        return True

    def map(self, data: dict, file_type: DatasetFormat) -> dict[str, list[str]]:
        return {DatasetFormat.JSON: self.__map_json(data)}.get(file_type)

    @abstractmethod
    def __map_json(self, data):
        pass

    # TODO: add another format in future, now just prepare json format + dataset from huggingFace
