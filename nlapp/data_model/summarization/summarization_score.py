from dataclasses import dataclass


@dataclass
class SummarizationScore:
    text: str
    summary: str
    rouge_2_recall: float
    rouge_2_precision: float
