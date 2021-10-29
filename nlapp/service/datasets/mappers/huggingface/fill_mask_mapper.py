from datasets.dataset_dict import DatasetDict
from nlapp.service.datasets.mappers.huggingface.dataset_mapper import (
    DatasetMapper,
)


class FillMaskMapper(DatasetMapper):
    dataset_type = "train"
    column_names = ["sentence", "target"]

    def __init__(self) -> None:
        super().__init__()
        self.subset_names = dict()

    def map(self, dataset: DatasetDict) -> dict[str, list[str]]:
        mapped_data = dict()
        data = dataset.data.get(self.dataset_type)
        data_columns = data.columns
        schema_info = data.schema

        for i, field in enumerate(schema_info):
            if self.column_names.__contains__(field):
                column = [x.as_py() for x in data_columns[0]]
                mapped_data[field] = column

        return mapped_data

    def is_correct(self, dataset: dict, dataset_name: str) -> bool:
        subset_name, subset = list(dataset.items())[0]
        splits = subset.get("splits")

        if splits.get(self.dataset_type) is None:
            return False

        counter = 0

        for feature in subset.get("features").keys():
            if self.column_names.__contains__(feature):
                counter += 1

        if counter == len(self.column_names):
            self.subset_names[dataset_name] = subset_name
            return True

        return False
