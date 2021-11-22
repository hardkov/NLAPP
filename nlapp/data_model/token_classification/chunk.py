from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Chunk:
    sentence: str
    tokens: List[Tuple]
