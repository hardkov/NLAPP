from dataclasses import dataclass
from typing import Dict, List

from transformers import pipeline


@dataclass
class AnswerScore:
    answer: str
    score: float


@dataclass
class QuestionAnsweringResult:
    context: str
    question: str
    expected_answer: str
    answer: AnswerScore


def evaluate(context: str, question: str, model, tokenizer) -> AnswerScore:
    question_answering = pipeline(
        "question-answering", model=model, tokenizer=tokenizer
    )

    qa_input = {"question": question, "context": context}

    result = question_answering(qa_input)
    return AnswerScore(result.get("answer"), result.get("score"))


def evaluate_dataset(
    dataset: Dict[str, List[str]], model, tokenizer
) -> List[QuestionAnsweringResult]:
    result = list()
    contexts = dataset.get("context")
    questions = dataset.get("context")
    answers = dataset.get("answers")

    for i in range(0, len(contexts)):
        answer_score = evaluate(contexts[i], questions[i], model, tokenizer)
        question_answer_result = QuestionAnsweringResult(
            contexts[i], questions[i], answers[i], answer_score
        )
        result.append(question_answer_result)

    return result
