from dataclasses import dataclass


@dataclass
class TokenClassificationPartResult:
    word: str
    score: float
    entity: str
    start: int
    end: int
