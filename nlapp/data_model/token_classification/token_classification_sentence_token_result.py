from dataclasses import dataclass
from typing import List
from nlapp.data_model.token_classification.token_classification_part_result import (
    TokenClassificationPartResult,
)


@dataclass
class TokenClassificationSentenceTokenResult:
    sentence_token: str
    expected_tag: str
    result_list: List[TokenClassificationPartResult]
    score_avg: float
