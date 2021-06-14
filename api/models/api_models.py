import requests
import logging
import requests
import asyncio

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
        url =  "https://huggingface.co/api/models"
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
                    task_type = TaskType.from_str(model["pipeline_tag"])
                    description = ""
                    models[name] = Model(name, description, task_type)

        return models


    #TODO fix function
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
            print(response.content)
            description = response.content
            self._models[name].description = description

    def by_task_type_models(self, task_type: TaskType):
        return dict(filter(lambda m: m[1].task_type == task_type, self._models.items()))

    def download_model(self,task_type: TaskType, name:str):
        if self._models[name] is None:
            raise Exception("Models name is incorrect.")
        if self._models[name].task_type != task_type:
            raise Exception("Models name is incorrect.")
        model = self._models[name]
        self.cache_model(model)


    # TODO : make generic function, working not only for one example
    def cache_model(self, model: Model):

        from transformers import AlbertTokenizer, AlbertForMaskedLM
        tokenizer = AlbertTokenizer.from_pretrained(model.name, cache_dir=ModelDir.cache_dir(model))
        model = AlbertForMaskedLM.from_pretrained(model.name, cache_dir=ModelDir.cache_dir(model))
        inputs = tokenizer("The capital of France is [MASK].", return_tensors="pt")
        outputs = model(**inputs)
        loss = outputs.loss
        logits = outputs.logits

