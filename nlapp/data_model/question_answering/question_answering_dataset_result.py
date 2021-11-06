from dataclasses import dataclass
from typing import List

from nlapp.data_model.question_answering.question_answering_result import (
    QuestionAnsweringResult,
)


@dataclass
class QuestionAnsweringDatasetResult:
    score_avg: float
    result_list: List[QuestionAnsweringResult]
