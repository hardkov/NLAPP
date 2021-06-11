import sys

from enum import Enum

DATASETS_DIR = sys.path[1] + '/data'


class DatasetDir(Enum):
    FILL_MASK = DATASETS_DIR + '/fillMask'
