import streamlit as st

from nlapp.controller.evaluation_controller import (
    evaluate_summarization,
    evaluate_dataset_summarization,
)
from nlapp.view.components.evaluation.evaluation_view import EvaluationView


class SummarizationEvaluation(EvaluationView):
    def display_predicts(self, title, list):
        with st.expander(title):
            st.table(
                [
                    {
                        "Text": we.text,
                        "Summary": we.summary,
                        "Recall (Rouge2)": we.rouge_2_recall,
                        "Precision (Rouge2)": we.rouge_2_precision,
                    }
                    for we in list
                ]
            )

    def display_manual_input(self, model, tokenizer):
        form = st.form(key="summarization-form")
        text = form.text_area(
            "Text",
            value="The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, "
            "and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each "
            "side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the "
            "tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building "
            "in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. "
            "Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller "
            "than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the "
            "second tallest free-standing structure in France after the Millau Viaduct. ",
        )

        submit = form.form_submit_button("Evaluate")

        if submit:
            result = evaluate_summarization(text, model, tokenizer)

            st.markdown("**Summary:**")
            st.info(result.summary)

    def display_dataset_input(self, model, tokenizer, dataset, timeout_seconds):
        results = evaluate_dataset_summarization(
            dataset, model, tokenizer, timeout_seconds=10
        )

        st.markdown(
            f"__Average recall (Rouge2):__ {results.rouge_2_recall_avg}"
        )
        st.markdown(
            f"__Average precision (Rouge2):__ {results.rouge_2_precision_avg}"
        )
        self.display_predicts("See predictions", results.summaries)
