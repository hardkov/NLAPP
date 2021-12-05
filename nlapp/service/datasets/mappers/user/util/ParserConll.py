import re


class ParserConll:
    @staticmethod
    def parse(file_string):
        data = ParserConll.get_lines_to_array(file_string)
        data = ParserConll.extract_sentence(data)
        data = ParserConll.remove_new_lines(data)
        data = ParserConll.extract_rows_from_chunks(data)
        data = ParserConll.remove_comments(data)
        data = ParserConll.extract_columns_from_rows(data)
        data = ParserConll.remove_tabulations_and_empty_spaces(data)

        return data

    @staticmethod
    def get_lines_to_array(file_string):
        return file_string.strip("\n")

    @staticmethod
    def extract_sentence(data):
        return re.split(r"(\r?\n){2,}", data)

    @staticmethod
    def remove_new_lines(data):
        return list(filter(lambda x: x != "\n", data))

    @staticmethod
    def remove_comments(data):
        return [list(filter(lambda x: len(x) > 0 and x[0] != "#", row)) for row in data]

    @staticmethod
    def extract_rows_from_chunks(data):
        return [s.split("\n") for s in data]

    @staticmethod
    def extract_columns_from_rows(data):
        return [[re.split(r"(\s){1,}", x) for x in row] for row in data]

    @staticmethod
    def remove_tabulations_and_empty_spaces(data):
        return [
            [list(filter(lambda x: x != "\t" and x != " ", ele)) for ele in row]
            for row in data
        ]
