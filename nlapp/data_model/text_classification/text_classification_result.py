from dataclasses import dataclass
from typing import List

from nlapp.data_model.text_classification.label_score import LabelScore


@dataclass
class TextClassificationResult:
    sentence: str
    expected_label: str
    labels: List[LabelScore]
