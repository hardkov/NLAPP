import nlapp.service.datasets.dataset_gateway as datasets_service
import nlapp.service.models.model_gateway as models_service
from nlapp.data_model.task_type import TaskType
import nlapp.service.evaluation.fill_mask_evaluation as fill_mask_evaluation_service


def get_datasets_by_task_type(task_type: TaskType):
    return datasets_service.get_datasets_by_task_type(task_type)


def get_models_by_task_type(task_type: TaskType):
    return models_service.get_models_by_task_type(task_type)


def fetch_description(model_name: str):
    models_service.fetch_description(model_name)


def evaluate_sentence(sentence: str, model, tokenizer):
    return fill_mask_evaluation_service.evaluate_sentence(sentence, model, tokenizer)


def evaluate_dataset(dataset, model, tokenizer, timeout_seconds):
    return fill_mask_evaluation_service.evaluate_dataset(dataset, model, tokenizer, timeout_seconds)


def download_model(task_type: TaskType, name: str):
    return models_service.download_model(task_type, name)


def download_dataset(task_type: TaskType, dataset_name: str):
    return datasets_service.download_dataset(task_type, dataset_name)

