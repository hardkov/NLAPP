import statistics
import timeit

from typing import Dict, List

from transformers import pipeline

from nlapp.data_model.token_classification.token_classification_part_result import (
    TokenClassificationPartResult,
)

from nlapp.data_model.token_classification.token_classification_sentence_token_result import (
    TokenClassificationSentenceTokenResult,
)

from nlapp.data_model.token_classification.token_classification_dataset_result import (
    TokenClassificationDatasetResult,
)


def evaluate(sentence, model, tokenizer) -> List[TokenClassificationPartResult]:
    token_classification = pipeline("ner", model=model, tokenizer=tokenizer)
    results = token_classification(sentence)
    tc_part_results = []
    for result in results:
        word = result.get("word")
        score = result.get("score")
        entity = result.get("entity")
        start = result.get("start")
        end = result.get("end")
        tc_part_result = TokenClassificationPartResult(
            word, score, entity, start, end
        )
        tc_part_results.append(tc_part_result)
    return tc_part_results


def evaluate_dataset(
    dataset: Dict[str, List], model, tokenizer, timeout_seconds=180
) -> TokenClassificationDatasetResult:
    wrong_predictions = list()
    correct_predictions = list()
    chunks = dataset.get("chunks")

    start = timeit.default_timer()
    for chunk in chunks:
        tc_part_results = evaluate(chunk.sentence, model, tokenizer)
        is_correct, result = is_correct_prediction(tc_part_results, chunk)

        if is_correct is True:
            correct_predictions.append(result)
        elif is_correct is False:
            wrong_predictions.append(result)

        if timeit.default_timer() - start > timeout_seconds:
            break

    scores_dataset = list(
        map(lambda x: x.score_avg, wrong_predictions + correct_predictions)
    )
    return TokenClassificationDatasetResult(
        statistics.mean(scores_dataset), wrong_predictions, correct_predictions
    )


def is_correct_prediction(
    predictions: List[TokenClassificationPartResult], chunk
):
    if len(predictions) > 0:
        scores = list(map(lambda r: r.score, predictions))
        mean = statistics.mean(scores)
    else:
        mean = 0.0

    found_tokens = list(map(lambda r: (r.word, r.entity), predictions))
    wrong_tags, correct_tags = list(), list()

    for token in found_tokens:
        if chunk.tokens.__contains__(token):
            correct_tags.append(token)
        else:
            wrong_tags.append(token)

    token_classification_result = TokenClassificationSentenceTokenResult(
        chunk.sentence, chunk.tokens, correct_tags, wrong_tags, mean
    )

    if len(wrong_tags) == 0 and len(correct_tags) >= len(chunk.tokens):
        return True, token_classification_result

    return False, token_classification_result
