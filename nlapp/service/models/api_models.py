import logging

import requests

from transformers import AutoModelForMaskedLM, AutoTokenizer
from nlapp.data_model.model import Model
from nlapp.service.models.model_dir import ModelDir
from nlapp.data_model.task_type import TaskType

from .string_utils.extract_part import find_between

logger = logging.getLogger(__name__)


class ApiModels:
    def get_models(self):
        return self.__init_models()

    @staticmethod
    def __init_models():
        models = dict()
        url = "https://huggingface.co/api/models"
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(
                "Status code of website %s for is %s"
                % (url, response.status_code)
            )
        else:
            json = response.json()
            logger.info("All models loaded")
            for model in json:
                if "pipeline_tag" in model:
                    name = str(model["modelId"])
                    try:
                        task_type = TaskType.from_str(model["pipeline_tag"])
                        description = ""
                        models[name] = Model(name, description, task_type)
                    except NotImplementedError:
                        # logger.info("This type of task is not supported.")
                        continue

        return models

    @staticmethod
    def fetch_description(model: Model) -> str:
        name = model.name

        main_url = "https://huggingface.co"
        description_url = f"{main_url}/{name}/resolve/main/README.md"
        response = requests.get(description_url)

        if response.status_code != 200:
            logger.error(
                "Status code of website %s for is %s"
                % (description_url, response.status_code)
            )
        else:
            description = response.content
            description = str(description, "utf-8")
            description = find_between(description, "#", "##")
            return description

    @staticmethod
    def download_model(model_info: Model):
        name = model_info.name

        # TODO:create generic solution for each type of task
        model_object = AutoModelForMaskedLM.from_pretrained(
            pretrained_model_name_or_path=name,
            cache_dir=ModelDir.cache_dir(model_info),
        )

        tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=name,
            cache_dir=ModelDir.cache_dir(model_info),
        )

        return model_object, tokenizer
