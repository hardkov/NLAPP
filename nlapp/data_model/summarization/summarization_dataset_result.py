from dataclasses import dataclass
from typing import List

from nlapp.data_model.summarization.summarization_score import (
    SummarizationScore,
)


@dataclass
class SummarizationDatasetResult:
    summaries: List[SummarizationScore]
    rouge_2_recall_avg: float
    rouge_2_precision_avg: float
