import json

import streamlit as st

from nlapp.controller.AppController import (
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


def write():
    task = st.session_state[KEYS.SELECTED_TASK]
    model = get_current_model()
    dataset = get_current_dataset()

    st.header("Results")

    should_download_model = st.checkbox("Toggle model fetching")

    if should_download_model:
        st.subheader("Manual input")

        model, tokenizer = download_model(task, model.name)

        form = st.form(key="my-form")
        value = form.text_input(
            task.name, value="Warsaw is the [MASK] of Poland."
        )
        form.form_submit_button("Evaluate")

        result_json = evaluate(model, tokenizer, value)
        html_code, height = html_creator.get_html_from_result_json(result_json)
        st.components.v1.html(html_code, height=height)

        st.subheader("Dataset input")
        dataset_input_enabled = st.button(
            "Download & Compute", key="dataset_input_enabled"
        )

        if dataset_input_enabled:
            dataset = download_dataset(task, dataset.name)
            results = evaluate_dataset(
                dataset, model, tokenizer, timeout_seconds=10
            )

            st.header("Results")
            st.markdown(
                f"__Number of evaluations:__ {results.all_evaluation_number}"
            )
            st.markdown(
                f"__Number of wrong evaluations:__ {results.wrong_evaluation_number}"
            )
            st.markdown(
                f"__Percent of wrong evaluations:__ {results.wrong_evaluation_percent}"
            )
            st.subheader("Wrong predicts")
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
