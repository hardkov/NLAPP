import os
import json
import logging
import git
from typing import Tuple

from datasets import load_dataset, list_datasets
from datasets.hf_api import ObjectInfo

from nlapp.data_model.dataset_dto import DatasetDTO
from nlapp.data_model.task_type import TaskType
from nlapp.service.datasets.mappers.huggingface.fill_mask_mapper import *

from nlapp.service.datasets.mappers.huggingface.question_answering_mapper import *
from nlapp.service.datasets.mappers.huggingface.text_classification_mapper import *
from pathlib import Path

from nlapp.service.datasets.mappers.huggingface.summarization_mapper import (
    SummarizationMapper,
)

hugging_face_dataset_mappers = {
    TaskType.FILL_MASK: FillMaskMapper(),
    TaskType.QUESTION_ANSWERING: QuestionAnsweringMapper(),
    TaskType.SUMMARIZATION: SummarizationMapper(),
    TaskType.TEXT_CLASSIFICATION: TextClassificationMapper(),
}

DATASET_DIR = os.path.join(
    Path(__file__).parent.parent.parent.parent.absolute(), "data", "datasets"
)

INFO_FILE_DIR = os.path.join(
    Path(__file__).parent.parent.parent.parent.absolute(),
    "data",
    "datasets_info",
)

logger = logging.getLogger(__name__)


class DatasetTool:
    available_mappers_flag = [
        TaskType.FILL_MASK,
        TaskType.QUESTION_ANSWERING,
        TaskType.SUMMARIZATION,
        TaskType.TEXT_CLASSIFICATION,
    ]

    def __init__(self, task_type: TaskType):
        self.task_type = task_type
        self.hugging_face_mapper = hugging_face_dataset_mappers.get(task_type)
        self.cached_dir = DATASET_DIR
        self.downloaded_info_dir = os.path.join(
            INFO_FILE_DIR, "datasets", "datasets"
        )
        self.info_file_name = "dataset_infos.json"
        self.__all_datasets = list_datasets(
            with_community_datasets=True, with_details=True
        )
        self.__execute_gh_clone()

    def get_datasets(self):
        return self.__init_datasets()

    def __execute_gh_clone(self):
        if self.create_dir(INFO_FILE_DIR):
            git.Git("data/datasets_info").clone(
                "https://github.com/huggingface/datasets"
            )

    def __init_datasets(self) -> Dict[str, DatasetDTO]:
        task_category = self.task_type.get_dataset_filter()
        specific_datasets = dict()

        for dataset in self.__all_datasets:
            if task_category in dataset.tags:
                if self.task_type in self.available_mappers_flag:
                    self.__check_dataset(dataset, specific_datasets)
                else:
                    specific_datasets[dataset.id] = DatasetDTO(
                        dataset.id, dataset.description, self.task_type
                    )

        logger.info(f"Dataset loaded: {self.task_type.name}")
        return specific_datasets

    def __check_dataset(self, dataset: ObjectInfo, datasets_dict: Dict) -> None:
        status, info_dict = self.__find_dataset_info(dataset.id)
        if (
            status is True
            and self.hugging_face_mapper.is_correct(info_dict, dataset.id)
            is True
        ):
            datasets_dict[dataset.id] = DatasetDTO(
                dataset.id, dataset.description, self.task_type
            )

    def __find_dataset_info(self, dataset_name: str) -> Tuple[bool, Dict]:
        for f in os.scandir(self.downloaded_info_dir):
            if f.is_dir() and f.name == dataset_name:
                for sub_f in os.scandir(f.path):
                    if sub_f.is_file() and sub_f.name == self.info_file_name:
                        data = open(sub_f.path)
                        return True, json.load(data)
        return False, dict()

    def download_dataset(self, name: str) -> Dict:
        self.create_dir(self.cached_dir)
        dataset_dict = self.__load_dateset(name)
        if self.task_type in self.available_mappers_flag:
            return self.hugging_face_mapper.map(dataset_dict)
        return dataset_dict

    def __load_dateset(self, name: str) -> DatasetDict:
        if self.hugging_face_mapper.subset_names.keys().__contains__(name):
            return load_dataset(
                name,
                self.hugging_face_mapper.subset_names[name],
                cache_dir=self.cached_dir,
            )
        return load_dataset(name, cache_dir=self.cached_dir)

    @staticmethod
    def create_dir(dataset_path: str) -> bool:
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)
            return True
        return False
