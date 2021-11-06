import os
from typing import Tuple

import requests
from datasets import load_dataset, list_datasets
from datasets.hf_api import ObjectInfo

from nlapp.data_model.dataset_dto import DatasetDTO
from nlapp.data_model.task_type import TaskType
from nlapp.service.datasets.mappers.huggingface.fill_mask_mapper import *
from nlapp.service.datasets.mappers.huggingface.question_answering_mapper import *
from pathlib import Path

from nlapp.service.datasets.mappers.huggingface.summarization_mapper import SummarizationMapper

hugging_face_dataset_mappers = {
    TaskType.FILL_MASK: FillMaskMapper(),
    TaskType.QUESTION_ANSWERING: QuestionAnsweringMapper(),
    TaskType.SUMMARIZATION: SummarizationMapper()
}


DATASET_DIR = os.path.join(
    Path(__file__).parent.parent.parent.parent.absolute(), "data", "datasets"
)


class DatasetTool:
    available_mappers_flag = [TaskType.FILL_MASK, TaskType.QUESTION_ANSWERING, TaskType.SUMMARIZATION]

    def __init__(self, task_type: TaskType):
        self.task_type = task_type
        self.hugging_face_mapper = hugging_face_dataset_mappers.get(task_type)
        self.cached_dir = DATASET_DIR
        self.github_repo = "https://raw.githubusercontent.com/huggingface/datasets/master/datasets/"
        self.info_file_name = "/dataset_infos.json"

    def get_datasets(self):
        return self.__init_datasets()

    def __init_datasets(self) -> Dict[str, DatasetDTO]:
        all_datasets = list_datasets(
            with_community_datasets=True, with_details=True
        )
        task_category = self.task_type.get_dataset_filter()
        specific_datasets = dict()

        for dataset in all_datasets:
            if task_category in dataset.tags:
                if self.task_type in self.available_mappers_flag:
                    self.__check_dataset(dataset, specific_datasets)
                else:
                    specific_datasets[dataset.id] = DatasetDTO(
                        dataset.id, dataset.description, self.task_type
                    )

        return specific_datasets

    def __check_dataset(self, dataset: ObjectInfo, datasets_dict: Dict) -> None:
        status, info_dict = self.__download_dataset_info(dataset.id)
        if (
            status is True
            and self.hugging_face_mapper.is_correct(info_dict, dataset.id)
            is True
        ):
            datasets_dict[dataset.id] = DatasetDTO(
                dataset.id, dataset.description, self.task_type
            )

    def __download_dataset_info(self, dataset_name: str) -> Tuple[bool, Dict]:
        url = self.github_repo + dataset_name + self.info_file_name
        resp = requests.get(url)
        return (
            (True, resp.json()) if resp.status_code < 400 else (False, dict())
        )

    def download_dataset(self, name: str) -> Dict:
        self.create_dir(self.cached_dir)
        dataset_dict = load_dataset(name, cache_dir=self.cached_dir)
        if self.task_type in self.available_mappers_flag:
            return self.hugging_face_mapper.map(dataset_dict)
        return dataset_dict

    @staticmethod
    def create_dir(dataset_path: str) -> None:
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)
