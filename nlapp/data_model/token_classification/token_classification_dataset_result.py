from dataclasses import dataclass
from typing import List
from nlapp.data_model.token_classification.token_classification_sentence_token_result import (
    TokenClassificationSentenceTokenResult,
)


@dataclass
class TokenClassificationDatasetResult:
    score_avg: float
    result_list: List[TokenClassificationSentenceTokenResult]
