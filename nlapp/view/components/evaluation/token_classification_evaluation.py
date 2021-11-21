import json
import streamlit as st
import functools

from nlapp.data_model.task_type import TaskType
from nlapp.view.helpers import html_creator
from nlapp.controller.evaluation_controller import (
    evaluate_token_classification,
    evaluate_dataset_token_classification,
)
from nlapp.view.components.evaluation.evaluation_view import EvaluationView


class TokenClassificationEvaluation(EvaluationView):
    def parse_result_to_json(self, result):
        token_score_list = list()
        for token_score in result.tokens_score:
            json_dict = dict()
            json_dict["token_str"] = token_score.token
            json_dict["score"] = token_score.score
            token_score_list.append(json_dict)
        return json.dumps(token_score_list)

    def display_manual_input(self, model, tokenizer):
        form = st.form(key="token-classification-form")
        value = form.text_input(
            "Sentence", value="My name is Sarah and I live in London"
        )
        form.form_submit_button("Evaluate")

        results = evaluate_token_classification(value, model, tokenizer)

        (
            html_code,
            height,
        ) = html_creator.get_token_classification_evaluation_html(
            value, results
        )
        st.components.v1.html(html_code, height=height)

    def display_dataset_input(self, model, tokenizer, dataset,  timeout_seconds):
        results = evaluate_dataset_token_classification(
            dataset, model, tokenizer, timeout_seconds=10
        )

        st.markdown(f"__Average score:__ {results.score_avg}")
        with st.expander("See wrong predictions"):
            st.table(
                [
                    {
                        "Sentence": we.sentence_token,
                        "Score average": we.score_avg,
                        "Predicts": functools.reduce(
                            lambda total, res: f"{total} {res.word}: {res.entity},",
                            we.result_list,
                            "",
                        ),
                        "Target": we.expected_tag,
                    }
                    for we in results.result_list
                ]
            )
