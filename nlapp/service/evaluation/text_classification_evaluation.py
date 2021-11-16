import statistics
import timeit

from typing import Dict, List

from transformers import pipeline

from nlapp.data_model.text_classification.label_score import LabelScore
from nlapp.data_model.text_classification.text_classification_result import (
    TextClassificationResult,
)
from nlapp.data_model.text_classification.text_classification_dataset_result import (
    TextClassificationDatasetResult,
)


def parse_result(result):
    result_list = []

    for item in result:
        result_list.append(LabelScore(item["label"], item["score"]))

    return result_list


def evaluate(sentence: str, model, tokenizer) -> List[LabelScore]:
    text_classification = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        return_all_scores=True,
    )

    output = text_classification(sentence)

    return parse_result(output[0])


def evaluate_dataset(
    dataset: Dict[str, List[str]], model, tokenizer, timeout_seconds=60
) -> TextClassificationDatasetResult:
    results = []

    texts = dataset.get("text")
    labels = dataset.get("label")

    start = timeit.default_timer()
    for i in range(len(texts)):
        labels_scores = evaluate(texts[i], model, tokenizer)
        text_classification_result = TextClassificationResult(
            texts[i], labels[i], labels_scores
        )

        results.append(text_classification_result)

        if timeit.default_timer() - start > timeout_seconds:
            break

    scores = list(map(lambda x: x.labels[0].score, results))
    return TextClassificationDatasetResult(
        statistics.mean(scores),
        results,
    )
