import statistics

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


def evaluate(
    single_token, model, tokenizer
) -> List[TokenClassificationPartResult]:
    token_classification = pipeline("ner", model=model, tokenizer=tokenizer)
    results = token_classification(single_token)
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
    dataset: Dict[str, List[str]], model, tokenizer
) -> TokenClassificationDatasetResult:
    result = list()
    tokens = dataset.get("tokens")
    ner_tags = dataset.get("ner_tags")

    for i in range(len(tokens)):

        tc_part_results = evaluate(tokens[i], model, tokenizer)
        scores = list(map(lambda r: r.score, tc_part_results))
        token_classification_result = TokenClassificationSentenceTokenResult(
            tokens[i], ner_tags[i], tc_part_results, statistics.mean(scores)
        )
        result.append(token_classification_result)

    scores_dataset = list(map(lambda x: x.score_avg, result))
    return TokenClassificationDatasetResult(
        statistics.mean(scores_dataset), result
    )
