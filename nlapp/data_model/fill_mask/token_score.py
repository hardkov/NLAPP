from dataclasses import dataclass


@dataclass
class TokenScore:
    token: str
    score: float
