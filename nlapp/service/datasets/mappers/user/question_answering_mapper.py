from conllu import parse
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
            mapped_data[column] = self.find_data_inside_json(
                mapped_column, data
            )
        return mapped_data

    def map_conll(self, data: str):
        mapped_data = dict()
        loaded_data = parse(data)
        sentences = loaded_data[0].metadata

        for column in self.column_mapping:
            mapped_column_prefix = self.column_mapping.get(column)
            mapped_data[column] = super().find_sentences_in_conllu_by_prefix(sentences, mapped_column_prefix)

        return mapped_data

    def validate_dataset(self, mapped_data: Dict[str, List[str]]) -> bool:
        return True

    def find_data_inside_json(self, mapped_column: str, json: Dict):
        return super().find_data_inside_json(mapped_column, json)
