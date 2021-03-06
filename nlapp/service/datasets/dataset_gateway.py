from typing import Any

from nlapp.data_model.dataset_dto import DatasetDTO
from nlapp.data_model.dataset_format import DatasetFormat
from nlapp.data_model.task_type import TaskType
from nlapp.service.datasets.dataset_tool import DatasetTool
from nlapp.service.datasets.mappers.user.fill_mask_mapper import *
from nlapp.service.datasets.mappers.user.text_classification_mapper import *
from nlapp.service.datasets.mappers.user.question_answering_mapper import *
from nlapp.service.datasets.mappers.user.summarization_mapper import *
from nlapp.service.datasets.mappers.user.token_classification_mapper import *
from nlapp.service.datasets.mappers.user.translation_mapper import *


DATASETS_LOADER = {
    TaskType.FILL_MASK: DatasetTool(TaskType.FILL_MASK),
    TaskType.TRANSLATION: DatasetTool(TaskType.TRANSLATION),
    TaskType.SUMMARIZATION: DatasetTool(TaskType.SUMMARIZATION),
    TaskType.TEXT_CLASSIFICATION: DatasetTool(TaskType.TEXT_CLASSIFICATION),
    TaskType.TOKEN_CLASSIFICATION: DatasetTool(TaskType.TOKEN_CLASSIFICATION),
    TaskType.QUESTION_ANSWERING: DatasetTool(TaskType.QUESTION_ANSWERING),
}


def __user_dataset_mapper_factory(
    task_type: TaskType,
    column_mapping: Dict[str, str],
    file_type: DatasetFormat,
) -> UserDatasetMapper:
    if task_type == TaskType.TEXT_CLASSIFICATION:
        return TextClassificationMapper(column_mapping)
    if task_type == TaskType.FILL_MASK:
        return FillMaskMapper(column_mapping)
    if task_type == TaskType.QUESTION_ANSWERING:
        return QuestionAnsweringMapper(column_mapping)
    if task_type == TaskType.SUMMARIZATION:
        return SummarizationMapper(column_mapping)
    if task_type == TaskType.TOKEN_CLASSIFICATION:
        return TokenClassificationMapper(column_mapping, file_type)
    if task_type == TaskType.TRANSLATION:
        return TranslationMapper(column_mapping)


def get_datasets_by_task_type(task_type: TaskType) -> Dict[str, DatasetDTO]:
    """
    Return dictionary of information about datasets for specific task.
    """
    return DATASETS_LOADER.get(task_type).get_datasets()


def get_dataset(task_type: TaskType, dataset_name: str) -> DatasetDTO:
    """
    Return information about specific dataset.
    """
    return get_datasets_by_task_type(task_type).get(dataset_name)


def download_dataset(task_type: TaskType, dataset_name: str) -> Dict:
    """
    1. Download dataset from huggingface.
    2. Mapped dataset to correct format.
    3. Return python dict.
    """
    return DATASETS_LOADER.get(task_type).download_dataset(dataset_name)


def map_user_dataset(
    task_type: TaskType,
    column_mapping: Dict[str, str],
    file_type: DatasetFormat,
    dataset: Any,
):
    """
    Return dataset mapped to correct format

    Args :
        - dataset is python dict, when you receive 'fill_mask_1.json' from user You can use json.load('fill_mask_1.json') to convert
        json file to python dict ; I not sure about CCL and CONLL -> they seem to be exotic and I need to check it.
        But for now we can use json file.
    """
    return __user_dataset_mapper_factory(
        task_type, column_mapping, file_type
    ).map(dataset, file_type)


def get_dataset_mapping_columns(task_type: TaskType):
    """
    Return mapping columns of dataset
    """
    return {
        TaskType.FILL_MASK: FillMaskMapper.columns,
        TaskType.QUESTION_ANSWERING: QuestionAnsweringMapper.columns,
        TaskType.SUMMARIZATION: SummarizationMapper.columns,
        TaskType.TEXT_CLASSIFICATION: TextClassificationMapper.columns,
        TaskType.TOKEN_CLASSIFICATION: TokenClassificationMapper.columns,
        TaskType.TRANSLATION: TranslationMapper.columns,
    }.get(task_type)
