import torch
import timeit

from api.models.model_gateway import download_model
from api.datasets.dataset_gateway import download_dataset
from dataclasses import dataclass
from api.task_type import TaskType
from typing import List


@dataclass
class TokenScore:
    token: str
    score: float


@dataclass
class FillMaskResult:
    sentence: str
    tokens_score: List[TokenScore]


def evaluate_sentence(sentence: str, model: str, task_type: TaskType, top=5):
    model, tokenizer = download_model(task_type, model)

    sentence = sentence.replace('[MASK]', tokenizer.mask_token)
    sentence = sentence.replace('<mask>', tokenizer.mask_token)

    inputs_ids = tokenizer.encode(sentence, return_tensors="pt")
    predictions = model.forward(inputs_ids)[0]

    mask_token_ids = torch.where(inputs_ids == tokenizer.mask_token_id)[1]
    mask_predictions = predictions[0, mask_token_ids, :]

    top_5_tokens = torch.topk(mask_predictions, k=top, dim=1).indices[0].tolist()
    scores = torch.softmax(mask_predictions, dim=1).tolist()[0]
    scores.sort(reverse=True)

    decoded_tokens = [TokenScore(tokenizer.decode(top_5_tokens[i]), scores[i]) for i in range(0, top)]
    return FillMaskResult(sentence, decoded_tokens)


# TODO: asynchronous evaluation and monitoring actual state of evaluation
def evaluate_dataset(dataset: str, model: str, task_type: TaskType, timeout_seconds=60):
    dataset = download_dataset(task_type, dataset)
    data = dataset.data.get('test_core')
    sentences = data.table.columns[0]

    results = list()
    start = timeit.default_timer()

    for sentence in sentences:
        results.append(evaluate_sentence(sentence.as_py(), model, task_type, top=1))
        if timeit.default_timer() - start > timeout_seconds:
            break

    return results
