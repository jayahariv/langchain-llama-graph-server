from langchain.llms.base import LLM
from .llm_providers.openai_provider import OpenAIProvider

class CustomLangChainLLM(LLM):
    def __init__(self, provider: OpenAIProvider):
        super().__init__()  # Call the parent class's constructor
        self._provider = provider  # Store the provider
    
    def _call(self, prompt: str, stop=None) -> str:
        return self.invoke(prompt)

    def invoke(self, prompt: str, stop=None) -> str:
        return self._provider.query(prompt)

    @property
    def _identifying_params(self):
        return {"provider": self._provider.__class__.__name__}

    @property
    def _llm_type(self):
        return "custom"

    @property
    def provider(self):
        return self._provider
