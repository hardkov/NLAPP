from dataclasses import dataclass


@dataclass
class LabelScore:
    label: str
    score: float
