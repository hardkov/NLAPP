from typing import Dict, List

from nlapp.service.datasets.mappers.user.dataset_mapper import UserDatasetMapper


class TranslationMapper(UserDatasetMapper):
    columns = ["source", "targets"]

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
        # return super().find_data_inside_json(mapped_column, json)
