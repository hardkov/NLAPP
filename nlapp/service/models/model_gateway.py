from nlapp.data_model.model import Model
from nlapp.service.models.api_models import ApiModels

api_models = ApiModels()


def get_models():
    """
    Return list of information about models for specific task.
    """
    return api_models.get_models()


# TODO : make function for more that only one model
def download_model(model: Model):
    """
    Download model from huggingface and return all data.
    """
    return api_models.download_model(model)


def fetch_description(model: Model):
    """
    Download description model from huggingface
    """
    return api_models.fetch_description(model)
