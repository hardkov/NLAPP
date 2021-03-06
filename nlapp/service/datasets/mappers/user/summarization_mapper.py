from typing import Dict, List

from nlapp.data_model.dataset_format import DatasetFormat
from nlapp.service.datasets.mappers.user.dataset_mapper import UserDatasetMapper


class SummarizationMapper(UserDatasetMapper):
    columns = ["text"]

    def __init__(self, column_mapping: Dict[str, str]):
        super().__init__(self.columns, column_mapping)

    def map_dataset(self, data: Dict, file_type) -> Dict[str, List[str]]:
        assert file_type == DatasetFormat.JSON
        mapped_data = dict()
        for column in self.columns:
            mapped_column = self.column_mapping.get(column)
            mapped_data[column] = self.find_data_inside_json(
                mapped_column, data
            )
        return mapped_data

    def validate_dataset(self, mapped_data: Dict[str, List[str]]) -> bool:
        return True

    def find_data_inside_json(self, mapped_column: str, json: Dict):
        return super().find_data_inside_json(mapped_column, json)
