from .llm_providers.base import LLMProvider

class CustomLangChainLLM:
    def __init__(self, provider: LLMProvider):
        super().__init__()
        self._provider = provider
        self.state_graph = None
    
    def load_model(self):
        self.provider.load_model()
        self.state_graph = self.build_state_graph()
    
    def build_state_graph(self):
        # Build and return the state graph
        pass
    
    def query(self, prompt):
        
        # Use the state graph to process the prompt
        
        response = self.provider.query(prompt)
        
        # Process response through the state graph
        
        return response

    @property
    def _identifying_params(self):
        return {"provider": self._provider.__class__.__name__}

    @property
    def _llm_type(self):
        return "custom"

    @property
    def provider(self):
        return self._provider
