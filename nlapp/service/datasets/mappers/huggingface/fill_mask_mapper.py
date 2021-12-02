from typing import Dict, List

from datasets.dataset_dict import DatasetDict

from nlapp.service.datasets.mappers.huggingface.dataset_mapper import (
    DatasetMapper,
)


class FillMaskMapper(DatasetMapper):
    split_type = "train"
    column_names = ["sentence", "target"]

    def __init__(self) -> None:
        super().__init__()
        self.subset_names = dict()

    def map(
        self, dataset: DatasetDict, dataset_name: str
    ) -> Dict[str, List[str]]:
        mapped_data = dict()
        data = dataset.data.get(self.split_type)
        data_columns = data.columns
        schema_info = data.schema

        for i, field in enumerate(schema_info):
            if self.column_names.__contains__(field.name):
                column = [x.as_py() for x in data_columns[i]]
                mapped_data[field.name] = column

        return mapped_data

    def is_correct(self, dataset: Dict, dataset_name: str) -> bool:
        subset_name, subset = list(dataset.items())[0]
        splits = subset.get("splits")

        if splits.get(self.split_type) is None:
            return False

        counter = 0

        for feature in subset.get("features").keys():
            if self.column_names.__contains__(feature):
                counter += 1

        if counter == len(self.column_names):
            self.subset_names[dataset_name] = subset_name
            return True

        return False
