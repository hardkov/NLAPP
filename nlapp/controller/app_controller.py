import time
from typing import Dict, List
import logging

import streamlit as st

import nlapp.service.datasets.dataset_gateway as datasets_service
import nlapp.service.models.model_gateway as models_service
from nlapp.data_model.dataset_dto import DatasetDTO
from nlapp.data_model.dataset_format import DatasetFormat
from nlapp.data_model.model_dto import ModelDTO
from nlapp.data_model.state import KEYS
from nlapp.data_model.task_type import TaskType

logger = logging.getLogger(__name__)


@st.cache(
    allow_output_mutation=True,
    max_entries=1,
)
def get_models_names(task_type: TaskType, cached: bool) -> List[str]:
    model_dict = get_models_by_task_type(task_type)
    model_list = list(model_dict.values())
    model_list_filtered = list(
        filter(lambda model: not cached or model.cached, model_list)
    )

    return list(map(lambda model: model.name, model_list_filtered))


@st.cache(
    allow_output_mutation=True,
    max_entries=1,
)
def get_datasets_names(task_type: TaskType, cached: bool) -> List[str]:
    dataset_dict = get_datasets_by_task_type(task_type)
    dataset_list = list(dataset_dict.values())
    dataset_list_filtered = list(
        filter(lambda dataset: not cached or dataset.cached, dataset_list)
    )

    return list(map(lambda dataset: dataset.name, dataset_list_filtered))


def get_current_model():
    model_name = st.session_state[KEYS.SELECTED_MODEL]
    task_type = st.session_state[KEYS.SELECTED_TASK]
    return get_models_by_task_type(task_type).get(model_name)


def get_current_dataset():
    if st.session_state[KEYS.UPLOAD_USER_DATASET_TOGGLED]:
        return st.session_state[KEYS.MAPPED_USER_DATASET]
    else:
        dataset_name = st.session_state[KEYS.SELECTED_DATASET]
        task_type = st.session_state[KEYS.SELECTED_TASK]
        return get_datasets_by_task_type(task_type).get(dataset_name)


def initialize_state():
    if st.session_state.get(KEYS.INITIALIZATION_DONE) is None:
        init_start = time.time()

        datasets = dict()
        models = dict()

        models_raw = models_service.get_models()

        for task_type in TaskType:
            datasets[
                task_type.name
            ] = datasets_service.get_datasets_by_task_type(task_type)
            models[task_type.name] = dict(
                filter(
                    lambda m: m[1].task_type == task_type, models_raw.items()
                )
            )

        st.session_state[KEYS.MODEL_LIST] = models
        st.session_state[KEYS.DATASET_LIST] = datasets
        st.session_state[KEYS.INITIALIZATION_DONE] = True
        st.session_state[KEYS.UPLOAD_USER_DATASET_TOGGLED] = False
        st.session_state[KEYS.MAPPED_USER_DATASET] = None

        init_end = time.time()
        logger.info(
            f"Initialization done, startup time: {init_end - init_start} seconds"
        )


def get_datasets_by_task_type(task_type: TaskType) -> Dict[str, DatasetDTO]:
    datasets = st.session_state.get(KEYS.DATASET_LIST)
    return datasets[task_type.name]


def get_models_by_task_type(task_type: TaskType) -> Dict[str, ModelDTO]:
    models = st.session_state.get(KEYS.MODEL_LIST)
    return models[task_type.name]


@st.cache(
    allow_output_mutation=True,
    max_entries=1,
)
def get_model_dto(task_type: TaskType, model_name: str) -> ModelDTO:
    models = get_models_by_task_type(task_type)
    model = models[model_name]

    if model is None:
        raise Exception("Models name is incorrect.")

    if model.description == "":
        model.description = models_service.fetch_description(model)

    return model


@st.cache(
    allow_output_mutation=True,
    max_entries=1,
)
def get_dataset_dto(task_type: TaskType, dataset_name: str) -> DatasetDTO:
    datasets = get_datasets_by_task_type(task_type)
    return datasets[dataset_name]


@st.cache(
    hash_funcs={"tokenizers.Tokenizer": id, "tokenizers.AddedToken": id, "torch.nn.parameter.Parameter": id},
    max_entries=1,
)
def download_model(task_type: TaskType, name: str):
    models = get_models_by_task_type(task_type)
    model = models[name]

    if model is None:
        raise Exception("Models name is incorrect.")

    return models_service.download_model(model)


@st.cache(
    hash_funcs={"pyarrow.lib.Buffer": id},
    allow_output_mutation=True,
    max_entries=1,
)
def download_dataset(task_type: TaskType, dataset_name: str):
    datasets = get_datasets_by_task_type(task_type)
    if datasets[dataset_name] is None:
        raise Exception("Dataset name is incorrect.")

    return datasets_service.download_dataset(task_type, dataset_name)


def get_dataset_mapping_columns(task_type: TaskType):
    return datasets_service.get_dataset_mapping_columns(task_type)


def load_user_dataset(
    task_type: TaskType,
    column_mapping: Dict[str, str],
    file_type: DatasetFormat,
    dataset: Dict,
) -> Dict[str, List[str]]:
    return datasets_service.map_user_dataset(
        task_type, column_mapping, file_type, dataset
    )
