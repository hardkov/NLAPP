import logging
import requests

from transformers import AutoModelForMaskedLM, AutoTokenizer
from api.models.model import Model
from api.models.model_dir import ModelDir
from api.task_type import TaskType

logger = logging.getLogger(__name__)


class ApiModels:
    def __init__(self):
        self._models = self.__init_models()

    def get_models(self):
        return self._models

    @staticmethod
    def __init_models():
        models = dict()
        url = "https://huggingface.co/api/models"
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(
                "Status code of website %s for is %s" % (url, response.status_code)
            )
        else:
            json = response.json()
            logger.info("All models loaded")
            for model in json:
                if "pipeline_tag" in model:
                    name = model['modelId']
                    try:
                        task_type = TaskType.from_str(model["pipeline_tag"])
                        description = ""
                        models[name] = Model(name, description, task_type)
                    except NotImplementedError:
                        # logger.info("This type of task is not supported.")
                        continue

        return models

    # TODO fix function
    def fetch_description(self, name: str):
        if self._models[name] is None:
            raise Exception("Models name is incorrect.")

        main_url = "https://huggingface.co"
        description_url = f"{main_url}/{name}/resolve/main/README.md"
        response = requests.get(description_url)

        if response.status_code != 200:
            logger.error(
                "Status code of website %s for is %s" % (description_url, response.status_code)
            )
        else:
            description = response.content
            self._models[name].description = description

    def by_task_type_models(self, task_type: TaskType):
        return dict(filter(lambda m: m[1].task_type == task_type, self._models.items()))

    def download_model(self, task_type: TaskType, name: str):
        if self._models[name] is None:
            raise Exception("Models name is incorrect.")

        if self._models[name].task_type != task_type:
            raise Exception("Models name is incorrect.")

        model_info = self._models[name]

        # TODO:create generic solution for each type of task
        model = AutoModelForMaskedLM.from_pretrained(
            pretrained_model_name_or_path=name,
            cache_dir=ModelDir.cache_dir(model_info)
        )

        tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=name,
            cache_dir=ModelDir.cache_dir(model_info)
        )


        return model, tokenizer
