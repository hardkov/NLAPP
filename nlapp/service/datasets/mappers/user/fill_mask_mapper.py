from typing import Dict, List

from nlapp.service.datasets.mappers.user.dataset_mapper import UserDatasetMapper


class FillMaskMapper(UserDatasetMapper):
    columns = ["sentence", "target"]

    def __init__(self, column_mapping: Dict[str, str]):
        super().__init__(self.columns, column_mapping)

    def map_json(self, data: Dict) -> Dict[str, List[str]]:
        mapped_data = dict()
        for column in self.columns:
            mapped_column = self.column_mapping.get(column)
            mapped_data[column] = self.__find_data_inside_json(
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

    @staticmethod
    def __find_data_inside_json(mapped_column: str, json: Dict):
        if mapped_column.__contains__("."):
            split_column = mapped_column.split(".")
            object_name = split_column[0]
            field_name = split_column[1]
            return [x[field_name] for x in json.get(object_name)]
        return json.get(mapped_column)
