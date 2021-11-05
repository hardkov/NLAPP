from typing import Dict, List

from datasets import DatasetDict

from nlapp.service.datasets.mappers.huggingface.dataset_mapper import DatasetMapper


class SummarizationMapper(DatasetMapper):
    split_type = "train"
    column_names = ["text"]

    def __init__(self) -> None:
        super().__init__()
        self.subset_names = dict()

    def map(self, dataset: DatasetDict) -> Dict[str, List[str]]:
        mapped_data = dict()
        data = dataset.data.get(self.split_type)
        data_columns = data.columns
        schema_info = data.schema

        for i, field in enumerate(schema_info):
            if field.name == self.column_names[0]:
                column = [x.as_py() for x in data_columns[i]]
                mapped_data[field.name] = column

        return mapped_data

    def is_correct(self, dataset: Dict, dataset_name: str) -> bool:
        subset_name, subset = list(dataset.items())[0]
        splits = subset.get("splits")

        if splits.get(self.split_type) is None:
            return False

        return subset.get("features").keys().contains(self.column_names[0])
