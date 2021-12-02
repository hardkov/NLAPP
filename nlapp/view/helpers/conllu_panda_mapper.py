import pandas as pd

from nlapp.service.datasets.mappers.user.util.ParserConll import ParserConll


def _make_columns(data):
    row = data[0]
    return [f"Column {ind + 1}" for ind, _ in enumerate(row)]


def flatten(t):
    return [item for sublist in t for item in sublist]


def map_conllu_df(file_string, **kwargs):
    data = ParserConll.parse(file_string)
    data = flatten(data)
    columns = _make_columns(data)
    df = pd.DataFrame(data=data, columns=columns)
    return df
