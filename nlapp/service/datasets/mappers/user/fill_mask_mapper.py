from typing import Dict, List

from nlapp.data_model.dataset_format import DatasetFormat
from nlapp.service.datasets.mappers.user.dataset_mapper import UserDatasetMapper


class FillMaskMapper(UserDatasetMapper):
    columns = ["sentence", "target"]

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
        if self.validate_dataset(mapped_data) is False:
            raise Exception(
                "Incorrect data format. Each sentence must contains [MASK] marker."
            )
        return mapped_data

    def validate_dataset(self, mapped_data: Dict[str, List[str]]) -> bool:
        for sentence in mapped_data[self.columns[0]]:
            if sentence.__contains__("[MASK]") is False:
                return False
        return True

    def find_data_inside_json(self, mapped_column: str, json: Dict):
        return super().find_data_inside_json(mapped_column, json)
