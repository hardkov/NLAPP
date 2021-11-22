from typing import Dict, List

from datasets.dataset_dict import DatasetDict

from nlapp.data_model.token_classification.chunk import Chunk
from nlapp.service.datasets.mappers.huggingface.dataset_mapper import (
    DatasetMapper,
)


class TokenClassificationMapper(DatasetMapper):
    split_type = "train"
    column_names = ["tokens", "ner_tags"]
    labels = dict()

    def __init__(self) -> None:
        super().__init__()
        self.subset_names = dict()

    def map(self, dataset: DatasetDict, dataset_name: str) -> Dict[str, List]:
        data = dataset.data.get(self.split_type)
        data_as_pydict = data.to_pydict()
        zip_data = zip(
            data_as_pydict[self.column_names[0]],
            data_as_pydict[self.column_names[1]],
        )

        chunks = list()
        for x, y in zip_data:
            chunk = self.create_chunk(x, y, dataset_name)
            if chunk is not None:
                chunks.append(chunk)

        return {"chunks": chunks}

    def create_chunk(self, tokens, tags, dataset_name):
        sentence = " ".join(tokens)
        dataset_labels = self.labels[dataset_name]
        tag_per_tokens = list()

        for x, y in zip(tokens, tags):
            if y != 0:
                tag_per_tokens.append((x, dataset_labels[y]))

        return (
            Chunk(sentence, tag_per_tokens) if len(tag_per_tokens) > 0 else None
        )

    def is_correct(self, dataset: Dict, dataset_name: str) -> bool:
        subset_name, subset = list(dataset.items())[0]
        splits = subset.get("splits")

        if splits.get(self.split_type) is None:
            return False

        counter = 0

        for feature in subset.get("features").keys():
            if feature == "ner_tags":
                status, labels = self.check_labels(
                    subset.get("features").get("ner_tags")
                )
                if status is False:
                    return False
                counter += 1
                self.labels[dataset_name] = labels
            elif self.column_names.__contains__(feature):
                counter += 1

        if counter == len(self.column_names):
            self.subset_names[dataset_name] = subset_name
            return True

        return False

    @staticmethod
    def check_labels(ner_tags):
        feature = ner_tags.get("feature")
        if feature is not None:
            labels = feature.get("names")
            if labels is not None:
                return True, labels
            return False, list()
        return False, list()
