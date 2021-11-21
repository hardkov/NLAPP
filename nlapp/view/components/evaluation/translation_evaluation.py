import streamlit as st

from nlapp.controller.evaluation_controller import (
    evaluate_translation,
    evaluate_dataset_translation,
)
from nlapp.view.components.evaluation.evaluation_view import EvaluationView


class TranslationEvaluation(EvaluationView):
    def display_predicts(self, title, list):
        with st.expander(title):
            st.table(
                [
                    {
                        "Text": we.translation_result.text,
                        "Expected translation": we.expected_translation,
                        "Translation": we.translation_result.text,
                        "BLEU": we.bleu,
                    }
                    for we in list
                ]
            )

    def display_manual_input(self, model, tokenizer):
        form = st.form(key="translation-form")
        text = form.text_input(
            "Text", value="My name is Wolfgang and I live in Berlin"
        )

        submit = form.form_submit_button("Evaluate")

        if submit:
            result = evaluate_translation(text, model, tokenizer)

            st.markdown("**Translation:**")
            st.info(result.translation)

    def display_dataset_input(self, model, tokenizer, dataset):
        results = evaluate_dataset_translation(
            dataset, model, tokenizer, timeout_seconds=10
        )

        st.markdown(f"__Average BLEU:__ {results.bleu_avg}")
        self.display_predicts("See predictions", results.translations_scores)
