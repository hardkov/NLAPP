from dataclasses import dataclass


@dataclass
class AnswerScore:
    answer: str
    score: float