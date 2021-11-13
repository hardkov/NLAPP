from dataclasses import dataclass
from typing import List

from nlapp.data_model.translation.translation_score import TranslationScore


@dataclass
class TranslationDatasetResult:
    bleu_avg: float
    translations_scores: List[TranslationScore]