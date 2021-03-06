from typing import Dict, List
import re

from nlapp.data_model.dataset_format import DatasetFormat
from nlapp.data_model.token_classification.chunk import Chunk
from nlapp.service.datasets.mappers.user.dataset_mapper import UserDatasetMapper
from nlapp.service.datasets.mappers.user.util.ParserConll import ParserConll


class TokenClassificationMapper(UserDatasetMapper):
    columns = ["tokens", "ner_tags", "tag_names"]

    def __init__(
        self, column_mapping: Dict[str, str], file_type: DatasetFormat
    ):
        if file_type == DatasetFormat.CONLL:
            self.columns = ["tokens", "ner_tags"]
        super().__init__(self.columns, column_mapping)

    def map_dataset(self, data, file_type):
        if file_type == DatasetFormat.JSON:
            return self.map_json(data)
        if file_type == DatasetFormat.CONLL:
            return self.map_conll(data)

    def map_json(self, data: Dict) -> Dict[str, List]:
        mapped_data = dict()
        for column in self.columns:
            mapped_column = self.column_mapping.get(column)
            column_data = self.find_data_inside_json(mapped_column, data)
            mapped_data[column] = column_data

        if self.validate_dataset(mapped_data) is False:
            raise Exception("Incorrect data format.")

        return {"chunks": self.__as_chunks(mapped_data)}

    def __as_chunks(self, mapped_data: Dict) -> List:
        tags = mapped_data["ner_tags"]
        tokens = mapped_data["tokens"]
        tag_names = mapped_data["tag_names"]
        chunks = list()

        for x, y in zip(tokens, tags):
            chunks.append(self.create_chunk(x, y, tag_names))

        return chunks

    @staticmethod
    def create_chunk(tokens: list, tags: list, tag_names: list):
        assert len(tokens) == len(tags)

        tokens_with_tags = list()
        for idx in range(0, len(tokens)):
            tag_idx = tags[idx]
            token = tokens[idx]
            if tag_idx != 0:
                tokens_with_tags.append((token, tag_names[tag_idx]))

        sentence = " ".join(tokens)
        return Chunk(sentence, tokens_with_tags)

    def validate_dataset(self, mapped_data: Dict[str, List[str]]) -> bool:
        return True

    def find_data_inside_json(self, mapped_column: str, json: Dict):
        return super().find_data_inside_json(mapped_column, json)

    def map_conll(self, file_string: str) -> Dict[str, List]:
        data = ParserConll.parse(file_string)
        token_nr_column = int(self.column_mapping["tokens"][7:]) - 1
        tag_nr_column = int(self.column_mapping["ner_tags"][7:]) - 1

        return {
            "chunks": self.__as_chunks_conll(
                data, token_nr_column, tag_nr_column
            )
        }

    def __as_chunks_conll(self, data, token_nr_column, tag_nr_column):
        chunks = list()
        for i in range(len(data)):
            chunks.append(
                self.create_chunk_conll(data[i], token_nr_column, tag_nr_column)
            )
        return chunks

    @staticmethod
    def create_chunk_conll(chunk_dataset, token_nr_column, tag_nr_column):
        tokens_with_tags = list()
        sentence = " ".join(list(zip(*chunk_dataset))[token_nr_column])
        for row in chunk_dataset:
            if row[tag_nr_column] != "O":
                tokens_with_tags.append(
                    (row[token_nr_column], row[tag_nr_column])
                )
        return Chunk(sentence, tokens_with_tags)
