import statistics

from typing import Dict, List

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
    dataset: Dict[str, List[str]], model, tokenizer
) -> QuestionAnsweringDatasetResult:
    result = list()
    contexts = dataset.get("context")
    questions = dataset.get("question")
    answers = dataset.get("answers")

    for i in range(0, len(contexts)):
        answer_score = evaluate(contexts[i], questions[i], model, tokenizer)
        question_answer_result = QuestionAnsweringResult(
            contexts[i], questions[i], answers[i], answer_score
        )
        result.append(question_answer_result)

    scores = list(map(lambda x: x.answer.score, result))
    return QuestionAnsweringDatasetResult(statistics.mean(scores), result)
