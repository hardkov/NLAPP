import pandas as pd


def _make_csv(data, i):
    fixed_lines = []
    raw_lines = data.splitlines()
    for line in raw_lines:
        if not line or line.startswith('#'):
            continue
        else:
            line = '%s\t%s' % (i, line)
            fixed_lines.append(line)
    return '\n'.join(fixed_lines)


def _make_columns(data):
    raw_lines = data[0].splitlines()
    line = raw_lines[0]
    return [f'Column {ind}' for ind, _ in enumerate(line.split("\t"))]


def map_conllu_df(file_string, **kwargs):
    import re
    from io import StringIO

    data = file_string.strip('\n')

    data = re.split(r'(\r?\n){2,}', data)
    data = list(filter(lambda el: el.strip() != "", data))
    csv = [_make_csv(sentence_data, i) for i, sentence_data in enumerate(data, start=1)]

    column_names = _make_columns(csv)

    csv = '\n\n'.join(csv)
    csv = StringIO(csv)

    df = pd.read_csv(csv, sep="\t", header=None, quoting=kwargs.pop('quoting', 3), names=column_names,
                     index_col=[0], engine='c', na_filter=False, **kwargs)
    return df
