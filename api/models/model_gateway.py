from api.models.api_models import ApiModels
from api.task_type import TaskType

api_models = ApiModels()


def get_models_by_task_type(task_type: TaskType):
    """
    Return list of information about models for specific task.
    """
    return api_models.by_task_type_models(task_type)


def get_model(task_type: TaskType, models_name: str):
    """
    Return information about specific model.
    """
    return get_models_by_task_type(task_type).get(models_name)


# TODO : make function for more that only one model
def download_model(task_type: TaskType, name: str = "albert-base-v2"):
    """
    Download model from huggingface and return all data.
    """
    return api_models.download_model(task_type, name)
