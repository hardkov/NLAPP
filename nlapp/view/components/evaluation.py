import json

import streamlit as st

from nlapp.controller.app_controller import (
    evaluate_sentence,
    evaluate_dataset,
    download_model,
    download_dataset,
    get_current_model,
    get_current_dataset,
)
from nlapp.data_model.state import KEYS
from nlapp.view.helpers import html_creator


def parse_result_to_json(result):
    token_score_list = list()
    for token_score in result.tokens_score:
        json_dict = dict()
        json_dict["token_str"] = token_score.token
        json_dict["score"] = token_score.score
        token_score_list.append(json_dict)
    return json.dumps(token_score_list)


def evaluate(model, tokenizer, value):
    result = evaluate_sentence(value, model, tokenizer)
    return parse_result_to_json(result)


def display_manual_input(task, model, tokenizer):
    form = st.form(key="my-form")
    value = form.text_input(task.name, value="Warsaw is the [MASK] of Poland.")
    form.form_submit_button("Evaluate")

    result_json = evaluate(model, tokenizer, value)
    html_code, height = html_creator.get_html_from_result_json(result_json)
    st.components.v1.html(html_code, height=height)


def should_not_evaluate_user_dataset():
    return not st.session_state[KEYS.UPLOAD_USER_DATASET_TOGGLED]


def does_mapped_user_dataset_exist():
    return st.session_state[KEYS.MAPPED_USER_DATASET] is not None


def display_dataset_input(task, model, tokenizer):
    dataset_input_enabled = False
    button_placeholder = st.empty()
    if should_not_evaluate_user_dataset():
        dataset_input_enabled = button_placeholder.button(
            "Download & Compute", key=KEYS.DATASET_INPUT_ENABLED
        )
    elif does_mapped_user_dataset_exist():
        dataset_input_enabled = button_placeholder.button(
            "Evaluate your dataset", key=KEYS.DATASET_INPUT_ENABLED
        )
    else:
        st.warning("There is no selected or loaded dataset")

    if dataset_input_enabled:
        dataset = get_current_dataset()
        if should_not_evaluate_user_dataset():
            dataset = download_dataset(task, dataset.name)
        results = evaluate_dataset(
            dataset, model, tokenizer, timeout_seconds=10
        )

        st.subheader("Results")
        st.markdown(
            f"__Number of evaluations:__ {results.all_evaluation_number}"
        )
        st.markdown(
            f"__Number of wrong evaluations:__ {results.wrong_evaluation_number}"
        )
        st.markdown(
            f"__Percent of wrong evaluations:__ {results.wrong_evaluation_percent}"
        )
        st.markdown("#### Wrong predicts")
        with st.expander("See predictions"):
            st.table(
                [
                    {
                        "Sentence": we.sentence,
                        "Predict token": we.token_score.token,
                        "Target": we.target,
                    }
                    for we in results.wrong_evaluations
                ]
            )


def write():
    task = st.session_state[KEYS.SELECTED_TASK]
    model = get_current_model()

    st.header("Results")

    should_download_model = st.checkbox(
        "Toggle model fetching", key=KEYS.MODEL_FETCHING_TOGGLED
    )
    if should_download_model:
        model, tokenizer = download_model(task, model.name)

        st.subheader("Dataset input")
        display_dataset_input(task, model, tokenizer)

        st.subheader("Manual input")
        display_manual_input(task, model, tokenizer)
