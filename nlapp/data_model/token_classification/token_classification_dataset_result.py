from dataclasses import dataclass
from typing import List
from nlapp.data_model.token_classification.token_classification_sentence_token_result import (
    TokenClassificationSentenceTokenResult,
)


@dataclass
class TokenClassificationDatasetResult:
    score_avg: float
    wrong_predictions: List[TokenClassificationSentenceTokenResult]
    correct_predictions: List[TokenClassificationSentenceTokenResult]
