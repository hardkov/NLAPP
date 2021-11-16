from dataclasses import dataclass

from nlapp.data_model.translation.translation_result import TranslationResult


@dataclass
class TranslationScore:
    translation_result: TranslationResult
    expected_translation: str
    bleu: float
