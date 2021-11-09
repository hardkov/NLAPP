import statistics

from typing import Dict, List
import timeit

from transformers import pipeline

from nlapp.data_model.question_answering.answer_score import AnswerScore
from nlapp.data_model.question_answering.question_answering_dataset_result import (
    QuestionAnsweringDatasetResult,
)
from nlapp.data_model.question_answering.question_answering_result import (
    QuestionAnsweringResult,
)


def evaluate(context: str, question: str, model, tokenizer) -> AnswerScore:
    question_answering = pipeline(
        "question-answering", model=model, tokenizer=tokenizer
    )

    qa_input = {"question": question, "context": context}

    result = question_answering(qa_input)
    return AnswerScore(result.get("answer"), result.get("score"))


def evaluate_dataset(
    dataset: Dict[str, List[str]], model, tokenizer, timeout_seconds=60
) -> QuestionAnsweringDatasetResult:
    result = list()
    contexts = dataset.get("context")
    questions = dataset.get("question")
    answers = dataset.get("answers")

    wrong_evaluations = list()
    right_evaluations = list()

    all_evaluation_number = 0
    wrong_evaluation_number = 0
    start = timeit.default_timer()

    for i in range(0, len(contexts)):
        all_evaluation_number += 1

        answer_score = evaluate(contexts[i], questions[i], model, tokenizer)
        question_answer_result = QuestionAnsweringResult(
            contexts[i], questions[i], answers[i], answer_score
        )
        predict_answer = question_answer_result.answer.answer
        if predict_answer not in question_answer_result.expected_answer:
            wrong_evaluation_number += 1
            wrong_evaluations.append(question_answer_result)
        else:
            right_evaluations.append(question_answer_result)

        result.append(question_answer_result)

        if timeit.default_timer() - start > timeout_seconds:
            break

    percent = wrong_evaluation_number / all_evaluation_number
    scores = list(map(lambda x: x.answer.score, result))
    return QuestionAnsweringDatasetResult(
        score_avg=statistics.mean(scores),
        all_evaluation_number=all_evaluation_number,
        wrong_evaluation_number=wrong_evaluation_number,
        wrong_evaluation_percent=percent,
        wrong_evaluations=wrong_evaluations,
        right_evaluations=right_evaluations,
    )
