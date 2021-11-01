from typing import Dict, List

from nlapp.service.datasets.mappers.user.dataset_mapper import UserDatasetMapper


class TextClassificationMapper(UserDatasetMapper):
    columns = []

    def __init__(
        self, column_mapping: Dict[str, str], number_of_sentence, has_idx,
    ):
        self.generate_name_for_columns(number_of_sentence, has_idx)
        super().__init__(self.columns, column_mapping)

    def generate_name_for_columns(self, number_of_sentence, has_idx):
        for i in range(1, number_of_sentence + 1):
            self.columns.append("sentence" + str(i))
        self.columns.append("label")
        if has_idx:
            self.columns.append("idx")

    def map_json(self, data: Dict) -> Dict[str, List[str]]:
        mapped_data = dict()
        for column in self.columns:
            mapped_column = self.column_mapping.get(column)
            mapped_data[column] = self.__find_data_inside_json(
                mapped_column, data
            )
        if self.validate_dataset(mapped_data) is False:
            raise Exception("Incorrect data format.")
        return mapped_data

    def validate_dataset(self, mapped_data: Dict[str, List[str]]) -> bool:
        return True

    @staticmethod
    def __find_data_inside_json(mapped_column: str, json: Dict):
        return super().find_data_inside_json(mapped_column, json)
