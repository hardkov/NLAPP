from dataclasses import dataclass
from typing import List
from nlapp.data_model.token_classification.token_classification_part_result import (
    TokenClassificationPartResult,
)


@dataclass
class TokenClassificationSentenceTokenResult:
    sentence: str
    expected_tags: List
    correct_tags: List
    wrong_tags: List
    score_avg: float
