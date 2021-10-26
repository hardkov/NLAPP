import streamlit as st
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
    return models_service.download_model(task_type, name)


@st.cache(
    hash_funcs={"pyarrow.lib.Buffer": id},
    allow_output_mutation=True,
    max_entries=1,
)
def download_dataset(task_type: TaskType, dataset_name: str):
    return datasets_service.download_dataset(task_type, dataset_name)

