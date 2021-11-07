from dataclasses import dataclass
from typing import List

from nlapp.data_model.text_classification.text_classification_result import (
    TextClassificationResult,
)


@dataclass
class TextClassificationDatasetResult:
    score_avg: float
    result_list: List[TextClassificationResult]
