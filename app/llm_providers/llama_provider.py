import os
from threading import Thread
import torch
import transformers
import time

from .base import LLMProvider
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

model_id = "meta-llama/Llama-3.2-1B"
# model_id = "distilgpt2"

# Global variables to manage model loading state
model_loading = False
model_loaded = False

# Placeholder for the model and tokenizer
model = None
pipeline = None

class LlamaProvider(LLMProvider):
    
    def __init__(self, model_name='{model_id}'):
        huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
        login(token = huggingface_token)

    def load_model(self):
        global model, model_loading, model_loaded, pipeline
        model_loading = True
        print("Starting model download...")

        pipeline = transformers.pipeline(
            "text-generation",
            model=model_id,
            device_map="auto",
        )

        print("Model download complete.")
        # this is to make sure, pipeline is loaded before we set model_loaded to True
        print(pipeline("Key to life is"))
        model_loaded = True
        model_loading = False
        print("Model loaded successfully.")
        

    def start_loading(self) -> dict:
        """Start the model loading process in a separate thread."""
        global model_loading
        if model_loading:
            return {"message": "Model is already being loaded."}, 400
        
        # Start model loading in a separate thread
        thread = Thread(target=self.load_model)
        thread.start()
        return {"message": "Model loading started."}, 202

    def get_loading_status(self) -> dict:
        global model, model_loading, model_loaded
        if model is not None:
            model_loaded = True
            model_loading = False
        
        if model_loading:
            return {"status": "loading"}, 200
        elif model_loaded:
            return {"status": "loaded"}, 200
        else:
            return {"status": "not-started"}, 200
    
    def query(self, prompt: str, **kwargs) -> dict:
        global pipeline
        result = pipeline(prompt, **kwargs)
        return result[0]['generated_text']