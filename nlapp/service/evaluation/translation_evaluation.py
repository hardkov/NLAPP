import statistics
import timeit


from typing import Dict, List
from datasets import load_metric

from nlapp.data_model.translation.translation_dataset_result import (
    TranslationDatasetResult,
)
from nlapp.data_model.translation.translation_result import TranslationResult
from nlapp.data_model.translation.translation_score import TranslationScore


def evaluate(batch, model, tokenizer):
    result = list()
    for portion in __split_text_to_smaller_portion(batch):
        inputs_ids = tokenizer.encode(portion, return_tensors="pt")
        output_ids = model.generate(input_ids=inputs_ids)[0]
        translation = tokenizer.decode(
            output_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )
        result.append(translation)
    joined_translations = "".join([item for item in result])

    return TranslationResult(batch, joined_translations)


def evaluate_dataset(
    dataset: Dict[str, List[str]], model, tokenizer, timeout_seconds=60
) -> TranslationDatasetResult:
    source = dataset.get("source")
    targets = dataset.get("targets")

    scores = list()

    start = timeit.default_timer()
    for i in range(len(source)):
        result = evaluate(source[i], model, tokenizer)
        bleu = calculate_bleu(targets[i], result.translation)
        score = TranslationScore(result, targets[i], bleu)
        scores.append(score)

        if timeit.default_timer() - start > timeout_seconds:
            break

    bleus = list(map(lambda x: x.bleu, scores))

    return TranslationDatasetResult(statistics.mean(bleus), scores)


def calculate_bleu(expected_translation, translation):
    metric = load_metric("bleu")
    prediction = list()
    if isinstance(translation, list) and len(translation) >= 1:
        translation = translation[0]
    prediction.append(convert(translation))
    reference = list()
    reference.append([])
    if isinstance(expected_translation, list) and len(expected_translation) >= 1:
        expected_translation = expected_translation[0]
    reference[0].append(convert(expected_translation))
    return metric.compute(predictions=prediction, references=reference)["bleu"]


def __split_text_to_smaller_portion(text: str, max_size=512) -> List[str]:
    portions = list()
    start, end = 0, max_size

    while start < len(text) and end - start > 256:
        portions.append(text[start:end])
        start = end + 1
        end = min(len(text), end + max_size)

    return portions


def convert(string):
    li = list(string.split(" "))
    return li
