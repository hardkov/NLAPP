import statistics

from typing import Dict, List

from transformers import pipeline

from nlapp.data_model.text_classification.label_score import LabelScore
from nlapp.data_model.text_classification.text_classification_result import (
    TextClassificationResult,
)
from nlapp.data_model.text_classification.text_classification_dataset_result import (
    TextClassificationDatasetResult,
)


def evaluate(sentence: str, model, tokenizer):
    text_classification = pipeline(
        "text-classification", model=model, tokenizer=tokenizer
    )

    tc_input = sentence

    result = text_classification(tc_input)
    label = result[0].get("label")
    score = result[0].get("score")
    return LabelScore(label, score)


def evaluate_dataset(
    dataset: Dict[str, List[str]], model, tokenizer
) -> TextClassificationDatasetResult:
    result = list()
    texts = dataset.get("text")
    labels = dataset.get("label")

    for i in range(len(texts)):
        label_score = evaluate(texts[i], model, tokenizer)
        text_classification_result = TextClassificationResult(
            texts[i], labels[i], label_score
        )
        result.append(text_classification_result)

    scores = list(map(lambda x: x.label.score, result))
    return TextClassificationDatasetResult(statistics.mean(scores), result)
