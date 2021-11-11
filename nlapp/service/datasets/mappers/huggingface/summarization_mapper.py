from typing import Dict, List

from datasets import DatasetDict

from nlapp.service.datasets.mappers.huggingface.dataset_mapper import (
    DatasetMapper,
)


class SummarizationMapper(DatasetMapper):
    split_type = "tests"
    column_names = {
        "text": [
            "text",
            "context",
            "abstract",
            "article",
            "document",
            "review",
            "body",
        ]
    }

    def __init__(self) -> None:
        super().__init__()
        self.subset_names = dict()

    def map(self, dataset: DatasetDict) -> Dict[str, List[str]]:
        mapped_column_name = list(self.column_names.keys())[0]
        accepted_column_names = self.column_names[mapped_column_name]

        mapped_data = dict()
        data = dataset.data.get(self.split_type)
        data_columns = data.columns
        schema_info = data.schema

        for i, field in enumerate(schema_info):
            if accepted_column_names.__contains__(field.name):
                column = [x.as_py() for x in data_columns[i]]
                mapped_data[mapped_column_name] = column
                break

        return mapped_data

    def is_correct(self, dataset: Dict, dataset_name: str) -> bool:
        subset_name, subset = list(dataset.items())[0]
        splits = subset.get("splits")

        if splits.get(self.split_type) is None:
            return False

        mapped_column_name = list(self.column_names.keys())[0]
        for accepted_column_name in self.column_names[mapped_column_name]:
            if subset.get("features").keys().__contains__(accepted_column_name):
                matched_feature = subset.get("features")[accepted_column_name]
                self.subset_names[dataset_name] = subset_name
                return self.__have_sub_feature(matched_feature) is False

        return False

    @staticmethod
    def __have_sub_feature(feature) -> bool:
        if isinstance(feature, Dict):
            sub_features = feature.get("feature")
            if sub_features is None:
                return False
            return True
        return False
