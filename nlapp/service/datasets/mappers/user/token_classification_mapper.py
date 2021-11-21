from typing import Dict, List

from nlapp.data_model.token_classification.chunk import Chunk
from nlapp.service.datasets.mappers.user.dataset_mapper import UserDatasetMapper


class TokenClassificationMapper(UserDatasetMapper):
    columns = ["tokens", "ner_tags", "tag_names"]

    def __init__(self, column_mapping: Dict[str, str]):
        super().__init__(self.columns, column_mapping)

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
