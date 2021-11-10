from dataclasses import dataclass
from typing import List

from nlapp.data_model.question_answering.question_answering_result import (
    QuestionAnsweringResult,
)


@dataclass
class QuestionAnsweringDatasetResult:
    score_avg: float
    all_evaluation_number: int
    wrong_evaluation_number: int
    wrong_evaluation_percent: float
    wrong_evaluations: List[QuestionAnsweringResult]
    right_evaluations: List[QuestionAnsweringResult]
