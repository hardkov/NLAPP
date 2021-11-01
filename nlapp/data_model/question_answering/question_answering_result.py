from dataclasses import dataclass

from nlapp.data_model.question_answering.answer_score import AnswerScore


@dataclass
class QuestionAnsweringResult:
    context: str
    question: str
    expected_answer: str
    answer: AnswerScore