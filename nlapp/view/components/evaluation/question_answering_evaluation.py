import json
import streamlit as st

from nlapp.data_model.task_type import TaskType
from nlapp.view.helpers import html_creator
from nlapp.controller.evaluation_controller import (
    evaluate_question_answering,
    evaluate_dataset_question_answering,
)
from nlapp.view.components.evaluation.evaluation_view import EvaluationView


class QuestionAnsweringEvaluation(EvaluationView):
    def parse_result_to_json(self, answer_score):
        json_dict = {}
        json_dict["token_str"] = answer_score.answer
        json_dict["score"] = answer_score.score
        return json.dumps([json_dict])

    def display_predicts(self, title, list):
        def get_expected_answer(obj):
            if isinstance(obj, str):
                return obj
            return obj[0]

        with st.expander(title):
            st.table(
                [
                    {
                        "Context": we.context,
                        "Question": we.question,
                        "Expected answer": get_expected_answer(
                            we.expected_answer
                        ),
                        "Predicted answer": we.answer.answer,
                    }
                    for we in list
                ]
            )

    def display_manual_input(self, model, tokenizer):
        form = st.form(key="question-form")
        title = form.header("Question Answering")
        question = form.text_input(
            "Question",
            value="Which name is also used to describe the Amazon rainforest in English?",
        )
        context = form.text_area(
            "Context",
            value="The Amazon rainforest (Portuguese: Floresta Amazônica or Amazônia; Spanish: Selva Amazónica, "
            "Amazonía or usually Amazonia; French: Forêt amazonienne; Dutch: Amazoneregenwoud), also known "
            "in English as Amazonia or the Amazon Jungle, is a moist broadleaf forest that covers most of the "
            "Amazon basin of South America. This basin encompasses 7,000,000 square kilometres (2,700,000 sq mi),"
            " of which 5,500,000 square kilometres (2,100,000 sq mi) are covered by the rainforest. "
            "This region includes territory belonging to nine nations. The majority of the forest is contained "
            "within Brazil, with 60% of the rainforest, followed by Peru with 13%, Colombia with 10%, and with "
            "minor amounts in Venezuela, Ecuador, Bolivia, Guyana, Suriname and French Guiana. States or "
            'departments in four nations contain "Amazonas" in their names. The Amazon represents over '
            "half of the planet's remaining rainforests, and comprises the largest and most biodiverse tract "
            "of tropical rainforest in the world, with an estimated 390 billion individual trees "
            "divided into 16,000 species.",
        )

        submit = form.form_submit_button("Evaluate")

        if submit:
            result = evaluate_question_answering(
                context, question, model, tokenizer
            )

            st.markdown(f"**Score:** {result.score}")
            st.progress(result.score)
            st.markdown("**Answer:**")
            st.info(result.answer)

    def display_dataset_input(self, model, tokenizer, dataset):
        results = evaluate_dataset_question_answering(
            dataset, model, tokenizer, timeout_seconds=10
        )

        st.subheader("Results")
        st.markdown(f"__Average score:__ {results.score_avg}")
        st.markdown(
            f"__Number of wrong evaluations:__ {results.wrong_evaluation_number}"
        )
        st.markdown(
            f"__Number of right evaluations:__ {results.all_evaluation_number - results.wrong_evaluation_number}"
        )
        st.markdown(
            f"__Percent of wrong evaluations:__ {int(results.wrong_evaluation_percent * 100)} %"
        )
        st.markdown("#### Wrong predicts")
        self.display_predicts(
            "See wrong predictions", results.wrong_evaluations
        )
        self.display_predicts(
            "See right predictions", results.right_evaluations
        )
