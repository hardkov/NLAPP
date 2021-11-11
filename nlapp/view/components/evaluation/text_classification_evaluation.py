import functools
import json

import streamlit as st

from nlapp.controller.evaluation_controller import evaluate_text_classification, evaluate_dataset_text_classification
from nlapp.view.components.evaluation.evaluation_view import EvaluationView
from nlapp.view.helpers import html_creator


class TextClassificationEvaluation(EvaluationView):
    def parse_result_to_json(self, result):
        label_score_list = list()
        for single_result in result:
            json_dict = dict()
            json_dict["token_str"] = single_result.label
            json_dict["score"] = single_result.score
            label_score_list.append(json_dict)
        return json.dumps(label_score_list)

    def display_predicts(self, title, predict_list):
        with st.expander(title):
            st.table(
                [
                    {
                        "Sentence": we.sentence,
                        "Labels": functools.reduce(lambda total, label: f'{total} {label.label}: {label.score},', we.labels, ""),
                    }
                    for we in predict_list
                ]
            )

    def display_manual_input(self, model, tokenizer):
        form = st.form(key="my-form")
        sentence = form.text_input(
            "Sentence",
            value="I like you. I love you"
        )
        form.form_submit_button("Evaluate")

        result = evaluate_text_classification(sentence, model, tokenizer)

        result_json = self.parse_result_to_json(result)
        html_code, height = html_creator.get_html_from_result_json(result_json)
        st.components.v1.html(html_code, height=height)

    def display_dataset_input(self, model, tokenizer, dataset):
        results = evaluate_dataset_text_classification(
            dataset, model, tokenizer, timeout_seconds=10
        )

        st.markdown(f"__Average top score:__ {results.score_avg}")
        self.display_predicts(
            "See predictions", results.result_list
        )
