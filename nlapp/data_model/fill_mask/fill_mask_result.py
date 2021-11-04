from dataclasses import dataclass
from typing import List

from nlapp.data_model.fill_mask.token_score import TokenScore


@dataclass
class FillMaskResult:
    sentence: str
    tokens_score: List[TokenScore]
