import streamlit as st

from nlapp.data_model.fill_mask.fill_mask_dataset_evaluation_result import FillMaskDatasetEvaluationResult
from nlapp.data_model.fill_mask.fill_mask_result import FillMaskResult
from nlapp.service.evaluation import fill_mask_evaluation as fill_mask_evaluation_service


@st.cache(
    hash_funcs={
        "tokenizers.Tokenizer": id,
        "tokenizers.AddedToken": id,
    },
    max_entries=1
)
def evaluate_fill_mask(sentence: str, model, tokenizer) -> FillMaskResult:
    return fill_mask_evaluation_service.evaluate_sentence(
        sentence, model, tokenizer
    )


@st.cache(
    hash_funcs={
        "pyarrow.lib.Buffer": id,
        "tokenizers.Tokenizer": id,
        "tokenizers.AddedToken": id,
    },
    max_entries=1
)
def evaluate_dataset_fill_mask(
    dataset, model, tokenizer, timeout_seconds
) -> FillMaskDatasetEvaluationResult:
    return fill_mask_evaluation_service.evaluate_dataset(
        dataset, model, tokenizer, timeout_seconds
    )
