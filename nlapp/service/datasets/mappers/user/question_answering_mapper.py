from typing import Dict, List

from nlapp.service.datasets.mappers.user.dataset_mapper import UserDatasetMapper


class QuestionAnsweringMapper(UserDatasetMapper):
    columns = ["context", "question", "answers"]

    def __init__(self, column_mapping: Dict[str, str]):
        super().__init__(self.columns, column_mapping)

    def map_json(self, data: Dict) -> Dict[str, List[str]]:
        mapped_data = dict()
        for column in self.columns:
            mapped_column = self.column_mapping.get(column)
            mapped_data[column] = self.__find_data_inside_json(
                mapped_column, data
            )
        return mapped_data

    def validate_dataset(self, mapped_data: Dict[str, List[str]]) -> bool:
        return True
