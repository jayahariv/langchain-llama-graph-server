from .base import LLMProvider
from openai import OpenAI

client = OpenAI()

class OpenAIProvider(LLMProvider):
    def __init__(self, model_name='gpt-4o-mini'):
        self.model_name = model_name

    def load_model(self):
        pass

    def get_loading_status(self) -> dict:
        return {"status": "loaded"}, 200
    
    def query(self, prompt: str, **kwargs) -> str:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt }],
            **kwargs
        )

        return completion.choices[0].message.content