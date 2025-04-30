# app/llm_providers/base.py
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def query(self, prompt: str, **kwargs) -> str:
        pass

    def get_loading_status(self) -> dict:
        pass

    def load_model(self) -> dict:
        pass
