from abc import ABC, abstractmethod


class EvaluationView(ABC):
    @abstractmethod
    def display_manual_input(self, model, tokenizer):
        pass

    @abstractmethod
    def display_dataset_input(self, model, tokenizer, dataset,  timeout_seconds):
        pass
