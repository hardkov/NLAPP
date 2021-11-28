from abc import ABC
from abc import abstractmethod
from typing import Dict, List

from nlapp.data_model.dataset_format import DatasetFormat


class UserDatasetMapper(ABC):
    columns = []

    def __init__(self, columns: List[str], column_mapping: Dict[str, str]):
        self.columns = columns
        self.column_mapping = column_mapping
        if self.validate_mapping() is False:
            raise Exception("Incorrect mapping.")

    def validate_mapping(self) -> bool:
        for column in self.columns:
            if self.column_mapping.get(column) is None:
                return False
        return True

    def map(self, data, file_type: DatasetFormat):
        return self.map_dataset(data, file_type)

    def find_data_inside_json(self, mapped_column: str, json: Dict):
        if mapped_column.__contains__("."):
            split_column = mapped_column.split(".")
            object_name = split_column[0]
            field_name = split_column[1]
            result = [x[field_name] for x in json.get(object_name)]
        else:
            result = json.get(mapped_column)
        if result is None:
            raise Exception("Incorrect mapping!")
        return result

    @abstractmethod
    def map_dataset(self, data, filetype):
        pass

    @abstractmethod
    def validate_dataset(self, mapped_data: Dict[str, List[str]]):
        pass

    # TODO: add another format in future, now just prepare json format + dataset from huggingFace
