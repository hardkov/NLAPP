from dataclasses import dataclass
from typing import List

from nlapp.data_model.fill_mask.fill_mask_dataset_sentence_evaluation import FillMaskDatasetSentenceEvaluation


@dataclass
class FillMaskDatasetEvaluationResult:
    all_evaluation_number: int
    wrong_evaluation_number: int
    wrong_evaluation_percent: float
    wrong_evaluations: List[FillMaskDatasetSentenceEvaluation]