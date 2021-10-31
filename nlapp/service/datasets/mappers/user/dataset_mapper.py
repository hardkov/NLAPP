from abc import ABC
from abc import abstractmethod
from typing import Dict, List

from nlapp.data_model.dataset_format import DatasetFormat


class UserDatasetMapper(ABC):
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

    def map(self, data: dict, file_type: DatasetFormat) -> Dict[str, List[str]]:
        return {DatasetFormat.JSON: self.map_json(data)}.get(file_type)

    @staticmethod
    def __find_data_inside_json(mapped_column: str, json: Dict):
        if mapped_column.__contains__("."):
            split_column = mapped_column.split(".")
            object_name = split_column[0]
            field_name = split_column[1]
            return [x[field_name] for x in json.get(object_name)]
        return json.get(mapped_column)

    @abstractmethod
    def map_json(self, data):
        pass

    @abstractmethod
    def validate_dataset(self, mapped_data: Dict[str, List[str]]):
        pass

    # TODO: add another format in future, now just prepare json format + dataset from huggingFace
