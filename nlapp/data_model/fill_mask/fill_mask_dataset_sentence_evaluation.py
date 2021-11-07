from dataclasses import dataclass

from nlapp.data_model.fill_mask.token_score import TokenScore


@dataclass
class FillMaskDatasetSentenceEvaluation:
    sentence: str
    token_score: TokenScore
    target: str
