from typing import List

import streamlit as st
from data_model.token_classification.token_classification_dataset_result import (
    TokenClassificationDatasetResult,
)
from data_model.token_classification.token_classification_part_result import (
    TokenClassificationPartResult,
)

from nlapp.data_model.question_answering.answer_score import AnswerScore
from nlapp.data_model.fill_mask.fill_mask_dataset_evaluation_result import (
    FillMaskDatasetEvaluationResult,
)
from nlapp.data_model.fill_mask.fill_mask_result import FillMaskResult
from nlapp.data_model.question_answering.question_answering_dataset_result import (
    QuestionAnsweringDatasetResult,
)
from nlapp.data_model.summarization.summarization_dataset_result import (
    SummarizationDatasetResult,
)
from nlapp.data_model.summarization.summarization_score import (
    SummarizationScore,
)
from nlapp.data_model.text_classification.label_score import LabelScore
from nlapp.data_model.text_classification.text_classification_dataset_result import (
    TextClassificationDatasetResult,
)
from nlapp.service.evaluation import (
    fill_mask_evaluation as fill_mask_evaluation_service,
    question_answering_evaluation as question_answering_service,
    summarization_evaluation as summarization_service,
    text_classification_evaluation as text_classification_service,
    token_classification_evaluation as token_classification_service,
)


@st.cache(
    hash_funcs={
        "tokenizers.Tokenizer": id,
        "tokenizers.AddedToken": id,
    },
    max_entries=1,
)
def evaluate_fill_mask(sentence: str, model, tokenizer) -> FillMaskResult:
    return fill_mask_evaluation_service.evaluate_sentence(
        sentence, model, tokenizer
    )


@st.cache(
    hash_funcs={
        "tokenizers.Tokenizer": id,
        "tokenizers.AddedToken": id,
    },
    max_entries=1,
)
def evaluate_question_answering(
    context: str, question: str, model, tokenizer
) -> AnswerScore:
    return question_answering_service.evaluate(
        context, question, model, tokenizer
    )


@st.cache(
    hash_funcs={
        "tokenizers.Tokenizer": id,
        "tokenizers.AddedToken": id,
        "torch.nn.parameter.Parameter": id,
    },
    max_entries=1,
)
def evaluate_summarization(text: str, model, tokenizer) -> SummarizationScore:
    return summarization_service.evaluate(text, model, tokenizer)


@st.cache(
    hash_funcs={
        "tokenizers.Tokenizer": id,
        "tokenizers.AddedToken": id,
    },
    max_entries=1,
)
def evaluate_text_classification(
    sentence: str, model, tokenizer
) -> List[LabelScore]:
    return text_classification_service.evaluate(sentence, model, tokenizer)


@st.cache(
    hash_funcs={
        "tokenizers.Tokenizer": id,
        "tokenizers.AddedToken": id,
    },
    max_entries=1,
)
def evaluate_token_classification(
    single_token: str, model, tokenizer
) -> List[TokenClassificationPartResult]:
    return token_classification_service.evaluate(single_token, model, tokenizer)


@st.cache(
    hash_funcs={
        "pyarrow.lib.Buffer": id,
        "tokenizers.Tokenizer": id,
        "tokenizers.AddedToken": id,
    },
    max_entries=1,
)
def evaluate_dataset_fill_mask(
    dataset, model, tokenizer, timeout_seconds
) -> FillMaskDatasetEvaluationResult:
    return fill_mask_evaluation_service.evaluate_dataset(
        dataset, model, tokenizer, timeout_seconds
    )


@st.cache(
    hash_funcs={
        "pyarrow.lib.Buffer": id,
        "tokenizers.Tokenizer": id,
        "tokenizers.AddedToken": id,
    },
    max_entries=1,
)
def evaluate_dataset_question_answering(
    dataset, model, tokenizer, timeout_seconds
) -> QuestionAnsweringDatasetResult:
    return question_answering_service.evaluate_dataset(
        dataset, model, tokenizer, timeout_seconds
    )


@st.cache(
    hash_funcs={
        "pyarrow.lib.Buffer": id,
        "tokenizers.Tokenizer": id,
        "tokenizers.AddedToken": id,
        "torch.nn.parameter.Parameter": id,
    },
    max_entries=1,
)
def evaluate_dataset_summarization(
    dataset, model, tokenizer, timeout_seconds
) -> SummarizationDatasetResult:
    return summarization_service.evaluate_dataset(
        dataset, model, tokenizer, timeout_seconds
    )


@st.cache(
    hash_funcs={
        "pyarrow.lib.Buffer": id,
        "tokenizers.Tokenizer": id,
        "tokenizers.AddedToken": id,
    },
    max_entries=1,
)
def evaluate_dataset_text_classification(
    dataset, model, tokenizer, timeout_seconds
) -> TextClassificationDatasetResult:
    return text_classification_service.evaluate_dataset(
        dataset, model, tokenizer, timeout_seconds
    )


@st.cache(
    hash_funcs={
        "pyarrow.lib.Buffer": id,
        "tokenizers.Tokenizer": id,
        "tokenizers.AddedToken": id,
    },
    max_entries=1,
)
def evaluate_dataset_token_classification(
    dataset, model, tokenizer, timeout_seconds
) -> TokenClassificationDatasetResult:
    return token_classification_service.evaluate_dataset(
        dataset, model, tokenizer, timeout_seconds
    )
