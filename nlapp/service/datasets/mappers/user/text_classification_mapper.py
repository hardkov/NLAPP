from typing import Dict, List

from nlapp.service.datasets.mappers.user.dataset_mapper import UserDatasetMapper


class TextClassificationMapper(UserDatasetMapper):
    columns = ["text", "label"]

    def __init__(self, column_mapping: Dict[str, str]):
        super().__init__(self.columns, column_mapping)

    def map_json(self, data: Dict) -> Dict[str, List[str]]:
        mapped_data = dict()
        for column in self.columns:
            mapped_column = self.column_mapping.get(column)
            mapped_data[column] = self.find_data_inside_json(
                mapped_column, data
            )
        if self.validate_dataset(mapped_data) is False:
            raise Exception("Incorrect data format.")
        return mapped_data

    def validate_dataset(self, mapped_data: Dict[str, List[str]]) -> bool:
        return True

    def find_data_inside_json(self, mapped_column: str, json: Dict):
        return super().find_data_inside_json(mapped_column, json)
