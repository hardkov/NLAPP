import statistics
import timeit
from typing import Dict, List

from rouge import Rouge

from nlapp.data_model.summarization.summarization_dataset_result import (
    SummarizationDatasetResult,
)
from nlapp.data_model.summarization.summarization_score import (
    SummarizationScore,
)


def evaluate(text: str, model, tokenizer) -> SummarizationScore:
    result = list()

    for portion in __split_text_to_smaller_portion(text):
        inputs_ids = tokenizer.encode(portion, return_tensors="pt")
        output_ids = model.generate(input_ids=inputs_ids)[0]
        summary = tokenizer.decode(
            output_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )
        result.append(calculate_rogue(portion, summary))

    rouge2_recalls = list(map(lambda x: x.rouge_2_recall, result))
    rouge2_precisions = list(map(lambda x: x.rouge_2_precision, result))
    joined_summary = "".join([item.summary for item in result])

    return SummarizationScore(
        text,
        joined_summary,
        statistics.mean(rouge2_recalls),
        statistics.mean(rouge2_precisions),
    )


def evaluate_dataset(
    dataset: Dict[str, List[str]], model, tokenizer, timeout_seconds=60
) -> SummarizationDatasetResult:
    result = list()
    texts = dataset.get("text")

    start = timeit.default_timer()
    for text in texts:
        summarization_score = evaluate(text, model, tokenizer)
        result.append(summarization_score)

        if timeit.default_timer() - start > timeout_seconds:
            break

    rouge2_recalls = list(map(lambda x: x.rouge_2_recall, result))
    rouge2_precisions = list(map(lambda x: x.rouge_2_precision, result))

    return SummarizationDatasetResult(
        result,
        statistics.mean(rouge2_recalls),
        statistics.mean(rouge2_precisions),
    )


def __split_text_to_smaller_portion(text: str, max_size=512) -> List[str]:
    portions = list()
    start, end = 0, max_size

    while start < len(text) and end - start > 256:
        portions.append(text[start:end])
        start = end + 1
        end = min(len(text), end + max_size)

    return portions


def calculate_rogue(text: str, summary: str) -> SummarizationScore:
    rouge_score = Rouge().get_scores(summary, text, avg=True)
    rouge_2 = rouge_score["rouge-2"]
    return SummarizationScore(
        text,
        summary,
        rouge_2_recall=rouge_2["r"],
        rouge_2_precision=rouge_2["p"],
    )
