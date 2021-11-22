import streamlit as st
import nlapp.view.components.evaluation.fill_mask_evaluation as fill_mask_evaluation_view
import nlapp.view.components.evaluation.question_answering_evaluation as question_answering_view
import nlapp.view.components.evaluation.summarization_evaluation as summarization_view
import nlapp.view.components.evaluation.text_classification_evaluation as text_classification_view
import nlapp.view.components.evaluation.token_classification_evaluation as token_classification_view
import nlapp.view.components.evaluation.translation_evaluation as translation_evaluation_view

from nlapp.controller.app_controller import (
    download_model,
    download_dataset,
    get_current_model,
    get_current_dataset,
    get_current_task,
)
from nlapp.data_model.state import KEYS
from nlapp.data_model.task_type import TaskType

EVALUATION_VIEWS = {
    TaskType.FILL_MASK: fill_mask_evaluation_view.FillMaskEvaluation(),
    TaskType.QUESTION_ANSWERING: question_answering_view.QuestionAnsweringEvaluation(),
    TaskType.SUMMARIZATION: summarization_view.SummarizationEvaluation(),
    TaskType.TEXT_CLASSIFICATION: text_classification_view.TextClassificationEvaluation(),
    TaskType.TOKEN_CLASSIFICATION: token_classification_view.TokenClassificationEvaluation(),
    TaskType.TRANSLATION: translation_evaluation_view.TranslationEvaluation()
}

ONE_YEAR_IN_SECONDS = 31556926

def should_not_evaluate_user_dataset():
    return not st.session_state[KEYS.UPLOAD_USER_DATASET_TOGGLED]


def does_mapped_user_dataset_exist():
    return st.session_state[KEYS.MAPPED_USER_DATASET] is not None


def get_submit_button_label():
    if (
            should_not_evaluate_user_dataset()
            and st.session_state.get(KEYS.SELECTED_DATASET) is not None
    ):
        return "Download & Compute"

    if does_mapped_user_dataset_exist():
        return "Evaluate your dataset"

    return None


def display_manual_input(task, model, tokenizer):
    EVALUATION_VIEWS[task].display_manual_input(model, tokenizer)


def display_dataset_input(task, model, tokenizer):
    evaluation_form = st.form("evaluation-form")

    label = get_submit_button_label()

    if label is None:
        st.warning("There is no selected or loaded dataset")
        return

    with evaluation_form:
        timeout_seconds = st.number_input("Computation timeout (seconds)", value=60,
                                          help="Type negative number in order to compute until the dataset is finished")
        dataset_input_enabled = st.form_submit_button(label)

    if dataset_input_enabled:
        dataset = get_current_dataset()
        if should_not_evaluate_user_dataset():
            dataset = download_dataset(task, dataset.name)

        real_timeout = timeout_seconds if timeout_seconds > 0 else ONE_YEAR_IN_SECONDS
        EVALUATION_VIEWS[task].display_dataset_input(model, tokenizer, dataset, real_timeout)


def write():
    task = get_current_task()
    model = get_current_model()

    st.header("Results")

    if model is None:
        st.info("No model is available")
        return

    should_download_model = st.checkbox(
        "Toggle model fetching", key=KEYS.MODEL_FETCHING_TOGGLED
    )
    if should_download_model:
        model, tokenizer = download_model(task, model.name)

        st.subheader("Dataset input")
        display_dataset_input(task, model, tokenizer)

        st.subheader("Manual input")
        display_manual_input(task, model, tokenizer)
