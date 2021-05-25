from datasets import load_dataset
from dataset import Dataset
from task_type import TaskType


class FillMaskDatasets:
    def __init__(self):
        self.datasets = self.__init_datasets()

    @staticmethod
    def __init_datasets():
        datasets = dict()
        name = 'numer_sense'
        description = 'NumerSense is a new numerical commonsense reasoning probing task, ' \
                      'with a diagnostic dataset consisting of 3,145 masked-word-prediction probes.' \
                      ' The general idea is to mask numbers between 0-10 in sentences mined from a commonsense' \
                      ' corpus and evaluate whether a language model can correctly predict the masked value'

        datasets[name] = Dataset(name, description, TaskType.FILL_MASK)
        return datasets

    def download_dataset(self, name):
        if self.datasets[name] is None:
            raise Exception("Dataset name is incorrect.")

        return load_dataset(name)



