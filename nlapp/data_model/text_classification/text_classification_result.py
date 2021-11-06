from dataclasses import dataclass

from nlapp.data_model.text_classification.label_score import LabelScore


@dataclass
class TextClassificationResult:
    sentence: str
    expected_label: str
    label: LabelScore
