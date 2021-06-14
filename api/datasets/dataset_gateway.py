from .dataset_tool import DatasetTool
from api.task_type import TaskType

DATASETS_LOADER = {
    TaskType.FILL_MASK: DatasetTool(TaskType.FILL_MASK),
    TaskType.TRANSLATION: DatasetTool(TaskType.TRANSLATION),
    TaskType.SUMMARIZATION: DatasetTool(TaskType.SUMMARIZATION),
    TaskType.TEXT_CLASSIFICATION: DatasetTool(TaskType.TEXT_CLASSIFICATION),
    TaskType.TOKEN_CLASSIFICATION: DatasetTool(TaskType.TOKEN_CLASSIFICATION),
    TaskType.QUESTION_ANSWERING: DatasetTool(TaskType.QUESTION_ANSWERING)
}


def get_datasets_by_task_type(task_type: TaskType):
    """
    Return dictionary of information about datasets for specific task.
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



