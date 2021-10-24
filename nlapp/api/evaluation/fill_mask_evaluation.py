import torch
import timeit

from dataclasses import dataclass
from typing import List


@dataclass
class TokenScore:
    token: str
    score: float


@dataclass
class FillMaskResult:
    sentence: str
    tokens_score: List[TokenScore]


@dataclass
class FillMaskDatasetSentenceEvaluation:
    sentence: str
    token_score: TokenScore
    target: str


@dataclass
class FillMaskDatasetEvaluationResult:
    all_evaluation_number: int
    wrong_evaluation_number: int
    wrong_evaluation_percent: float
    wrong_evaluations: List[FillMaskDatasetSentenceEvaluation]


def evaluate_sentence(sentence: str, model, tokenizer, top=5):
    sentence = sentence.replace("[MASK]", tokenizer.mask_token)
    sentence = sentence.replace("<mask>", tokenizer.mask_token)

    inputs_ids = tokenizer.encode(sentence, return_tensors="pt")
    predictions = model.forward(inputs_ids)[0]

    mask_token_ids = torch.where(inputs_ids == tokenizer.mask_token_id)[1]
    mask_predictions = predictions[0, mask_token_ids, :]

    top_5_tokens = (
        torch.topk(mask_predictions, k=top, dim=1).indices[0].tolist()
    )
    scores = torch.softmax(mask_predictions, dim=1).tolist()[0]
    scores.sort(reverse=True)

    decoded_tokens = [
        TokenScore(tokenizer.decode(top_5_tokens[i]), scores[i])
        for i in range(0, top)
    ]
    return FillMaskResult(sentence, decoded_tokens)


# # TODO: asynchronous evaluation and monitoring actual state of evaluation
def evaluate_dataset(dataset, model, tokenizer, timeout_seconds=60):
    data = dataset.data.get("train")
    sentences = data.table.columns[0]
    targets = data.table.columns[1]

    wrong_evaluations = list()
    start = timeit.default_timer()

    all_evaluation_number = 0
    wrong_evaluation_number = 0

    for sentence, target in zip(sentences, targets):
        all_evaluation_number += 1
        evaluate_result = evaluate_sentence(
            sentence.as_py(), model, tokenizer, top=1
        )
        token_score_top = evaluate_result.tokens_score[0]
        if token_score_top.token != target.as_py():
            wrong_evaluation_number += 1
            wrong_evaluation = FillMaskDatasetSentenceEvaluation(
                evaluate_result.sentence, token_score_top, target.as_py()
            )
            wrong_evaluations.append(wrong_evaluation)

        if timeit.default_timer() - start > timeout_seconds:
            break

    percent = wrong_evaluation_number / all_evaluation_number
    result = FillMaskDatasetEvaluationResult(
        all_evaluation_number=all_evaluation_number,
        wrong_evaluation_number=wrong_evaluation_number,
        wrong_evaluation_percent=percent,
        wrong_evaluations=wrong_evaluations,
    )

    return result
