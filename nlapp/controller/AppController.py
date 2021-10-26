from typing import Dict

import streamlit as st
import nlapp.service.datasets.dataset_gateway as datasets_service
import nlapp.service.models.model_gateway as models_service
from nlapp.data_model.dataset import Dataset
from nlapp.data_model.model import Model
from nlapp.data_model.state import KEYS
from nlapp.data_model.task_type import TaskType
import nlapp.service.evaluation.fill_mask_evaluation as fill_mask_evaluation_service


# to be refactored by initializator
def get_datasets_by_task_type(task_type: TaskType) -> Dict[str, Dataset]:
    datasets: Dict[str, Dict[str, Dataset]] = st.session_state.get(KEYS.DATASET_LIST)

    if datasets is None:
        st.session_state[KEYS.DATASET_LIST] = dict()
        datasets = st.session_state[KEYS.DATASET_LIST]

    if datasets.get(task_type.name) is None:
        datasets[task_type.name] = datasets_service.get_datasets_by_task_type(task_type)

    return datasets[task_type.name]


# to be refactored by initializator, types do not match for some reason
def get_models_by_task_type(task_type: TaskType) -> Dict[str, Model]:
    models = st.session_state.get(KEYS.MODEL_LIST)
    if models is None:
        st.session_state[KEYS.MODEL_LIST] = models_service.get_models()
        models = st.session_state.get(KEYS.MODEL_LIST)

    return dict(filter(lambda m: m[1].task_type == task_type, models.items()))


# to be refactored - no need to filter by task type
def fetch_description(model_name: str, task_type: TaskType):
    models = get_models_by_task_type(task_type)
    model = models[model_name]

    if model is None:
        raise Exception("Models name is incorrect.")

    # we will do mulitple requests if there is no description on the remote service
    if model.description is not "" and model.description is not None:
        return model.description

    model.description = models_service.fetch_description(model)

    return model.description


def evaluate_sentence(sentence: str, model, tokenizer):
    return fill_mask_evaluation_service.evaluate_sentence(sentence, model, tokenizer)


@st.cache(
    hash_funcs={
        "pyarrow.lib.Buffer": id,
        "tokenizers.Tokenizer": id,
        "tokenizers.AddedToken": id,
    }
)
def evaluate_dataset(dataset, model, tokenizer, timeout_seconds):
    return fill_mask_evaluation_service.evaluate_dataset(dataset, model, tokenizer, timeout_seconds)


@st.cache(
    hash_funcs={"tokenizers.Tokenizer": id, "tokenizers.AddedToken": id},
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

