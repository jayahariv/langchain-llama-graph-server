import re

from .llm_providers.base import LLMProvider
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal
from flask import jsonify
from .llm_providers.llama_provider import LlamaProvider
from .llm_providers.openai_provider import OpenAIProvider
            

class GraphState(TypedDict):
    query: str
    is_code_related: bool
    from_llama: bool
    response: str

class CustomLangChainLLM:
    def __init__(self):
        super().__init__()
        self.state_graph = None
        self.llama_provider = LlamaProvider()
        self.openai_provider = OpenAIProvider()
        self.loading_status = False
    
    def load_model(self):
        self.llama_provider.load_model()
        self.openai_provider.load_model()

        self.state_graph = self.build_state_graph()
        self.loading_status = True
    
    def build_state_graph(self):
        graph = StateGraph(GraphState)

        # Node to classify if the query is code-related
        def classify_query(state: GraphState) -> GraphState:
            query = state["query"].lower()
            code_patterns = [
                r"```",  # Code block
                r"\b(def|function|class|import|export|const|let|var|if|else|for|while|return)\b",  # Programming keywords
                r"\b(python|javascript|java|c\+\+|sql)\b",  # Language names
            ]
            is_code_related = any(re.search(pattern, query) for pattern in code_patterns)
            return {"is_code_related": is_code_related, "from_llama": False}
        
        def llama_provider_node(state: GraphState) -> GraphState:
            response = self.llama_provider.query(state["query"])
            return {"response": response, "from_llama": True}

        def openai_provider_node(state: GraphState) -> GraphState:
            response = self.openai_provider.query(state["query"])
            return {"response": response, "from_llama": False}
    
        # Add nodes
        graph.add_node("classify_query", classify_query)
        graph.add_node("llama_provider", llama_provider_node)
        graph.add_node("openai_provider", openai_provider_node)
        
        # Set entry point
        graph.set_entry_point("classify_query")

        # Conditional edge to route based on query type or LLaMA origin
        def route_query(state: GraphState) -> Literal["llama_provider", "openai_provider"]:
            if state["from_llama"]:
                return "openai_provider"
            
            return "llama_provider" if state["is_code_related"] else "openai_provider"
        
        # Add conditional edges
        graph.add_conditional_edges(
            "classify_query",
            route_query,
            {
                "llama_provider": "llama_provider",
                "openai_provider": "openai_provider"
            }
        )
        
        # Add edges to handle LLaMA follow-ups
        graph.add_edge("llama_provider", "openai_provider")
        graph.add_edge("openai_provider", END)
        
        return graph.compile()
    
    def query(self, prompt):
        if not self.loading_status:
            self.load_model()
        
        initial_state = GraphState(query=prompt, is_code_related=False, from_llama=False, response="")
        
        final_state = self.state_graph.invoke(initial_state)
        
        return {
            "response": final_state["response"],
            "is_code_related": final_state["is_code_related"],
            "from_llama": final_state["from_llama"]
        }

    @property
    def _identifying_params(self):
        return {"provider": self._provider.__class__.__name__}

    @property
    def _llm_type(self):
        return "custom"

    @property
    def provider(self):
        return self._provider
