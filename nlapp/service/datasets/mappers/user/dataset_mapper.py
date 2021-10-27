from nlapp.data_model.dataset_format import DatasetFormat


class UserDatasetMapper:
    def __init__(self, columns: list[str], column_mapping: dict[str, str]):
        self.columns = columns
        self.column_mapping = column_mapping
        if self.validate_mapping() is False:
            raise Exception("Incorrect mapping.")

    def validate_mapping(self) -> bool:
        for column in self.columns:
            if self.column_mapping.get(column) is None:
                return False
        return True

    def map(self, data: dict, file_type: DatasetFormat) -> dict[str, list[str]]:
        return {
            DatasetFormat.JSON: self.__map_json(data),
            DatasetFormat.CCL: self.__map_ccl(data),
            DatasetFormat.CONLL: self.__map_conll(data),
        }.get(file_type)

    def __map_json(self, data: dict) -> dict[str, list[str]]:
        mapped_data = dict()
        for column in self.columns:
            mapped_column = self.column_mapping.get(column)
            mapped_data[column] = self.__find_data_inside_json(
                mapped_column, data
            )
        return mapped_data

    @staticmethod
    def __find_data_inside_json(mapped_column: str, json: dict):
        if mapped_column.__contains__("."):
            split_column = mapped_column.split(".")
            object_name = split_column[0]
            field_name = split_column[1]
            return [x[field_name] for x in json.get(object_name)]
        return json.get(mapped_column)

    # check ccl format
    def __map_ccl(self, data: dict) -> dict[str, list[str]]:
        pass

    # check conll format
    def __map_conll(self, data: dict) -> dict[str, list[str]]:
        pass
