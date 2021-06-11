from .fill_mask_dataset import FillMaskDatasets
from .task_type import TaskType

DATASETS_LOADER = {
    TaskType.FILL_MASK: FillMaskDatasets()
}


def get_datasets_by_task_type(task_type: TaskType):
    """
    Return list of information about datasets for specific task.
    """
    return DATASETS_LOADER.get(task_type).get_datasets()


def get_dataset(task_type: TaskType, dataset_name: str):
    """
    Return information about specific dataset.
    """
    return get_datasets_by_task_type(task_type).get(dataset_name)


def download_dataset(task_type: TaskType, dataset_name: str):
    """
    Download dataset from huggingface and return all data.
    """
    return DATASETS_LOADER.get(task_type).download_dataset(dataset_name)



