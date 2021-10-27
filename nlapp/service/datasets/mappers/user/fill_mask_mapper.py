from nlapp.service.datasets.mappers.user.dataset_mapper import UserDatasetMapper
from nlapp.data_model.dataset_format import DatasetFormat


class FillMaskMapper:
    columns = ["sentence", "target"]

    def __init__(self, column_mapping: dict[str, str]):
        self.column_mapping = column_mapping
        self.mapper = UserDatasetMapper(self.columns, column_mapping)

    def map(self, data: dict, file_type: DatasetFormat):
        mapped_data = self.mapper.map(data, file_type)
        if self.__validate_dataset(mapped_data) is False:
            raise Exception(
                "Incorrect data format. Each sentence must contains [MASK] marker."
            )
        return mapped_data

    def __validate_dataset(self, mapped_data: dict[str, list[str]]) -> bool:
        for sentence in mapped_data[self.columns[0]]:
            if sentence.__contains__("[MASK]") is False:
                return False
        return True
