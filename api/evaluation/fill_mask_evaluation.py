import torch

from api.models.model_gateway import download_model
from api.datasets.dataset_gateway import download_dataset
from dataclasses import dataclass
from api.task_type import TaskType


@dataclass
class TokenScore:
    token: str
    score: float


@dataclass
class FillMaskResult:
    sentence: str
    tokens_score: list[TokenScore]


def evaluate(sentence: str, model: str, task_type: TaskType, top=5):
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


def evaluate_dataset(dataset: str, model: str, task_type: TaskType):
    dataset = download_dataset(task_type, dataset)
    data = dataset.data.get('test_core')
    sentences = data.table.columns[0]

    results = list()

    for sentence in sentences:
        print(sentence)
        results.append(evaluate(sentence.as_py(), model, task_type, top=1))

    print(results)
    return results
