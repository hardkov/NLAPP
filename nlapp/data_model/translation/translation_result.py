from dataclasses import dataclass


@dataclass
class TranslationResult:
    text: str
    translation: str
