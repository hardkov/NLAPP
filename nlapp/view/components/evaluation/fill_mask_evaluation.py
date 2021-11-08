import json
import streamlit as st

from nlapp.data_model.task_type import TaskType
from nlapp.view.helpers import html_creator
from nlapp.controller.evaluation_controller import evaluate_fill_mask, evaluate_dataset_fill_mask


def parse_result_to_json(result):
    token_score_list = list()
    for token_score in result.tokens_score:
        json_dict = dict()
        json_dict["token_str"] = token_score.token
        json_dict["score"] = token_score.score
        token_score_list.append(json_dict)
    return json.dumps(token_score_list)


def display_manual_input(model, tokenizer):
    form = st.form(key="my-form")
    value = form.text_input(TaskType.FILL_MASK.name, value="Warsaw is the [MASK] of Poland.")
    form.form_submit_button("Evaluate")

    result = evaluate_fill_mask(value, model, tokenizer)

    result_json = parse_result_to_json(result)
    html_code, height = html_creator.get_html_from_result_json(result_json)
    st.components.v1.html(html_code, height=height)


def display_dataset_input(model, tokenizer, dataset):
    results = evaluate_dataset_fill_mask(
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
