import os
import torch
import transformers
from threading import Thread
from transformers import AutoModelForCausalLM, pipeline

from .base import LLMProvider
from huggingface_hub import login
from accelerate import disk_offload

# model_id = "meta-llama/Llama-3.3-70B-Instruct"
model_id = "meta-llama/Llama-3.2-1B-Instruct"
# model_id = "distilgpt2"

# Global variables to manage model loading state
model_loading = False
model_loaded = False

# Placeholder for the model and tokenizer
model = None
pipe = None

class LlamaProvider(LLMProvider):
    
    def __init__(self, model_name='{model_id}'):
        huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
        login(token = huggingface_token)

    def load_model(self):
        global model, model_loading, model_loaded, pipe
        model_loading = True
        print("Starting model download...")

            # Load model for offloading
        self._model = AutoModelForCausalLM.from_pretrained(
            model_id, device_map="auto", offload_folder="offload",
            offload_state_dict=True, torch_dtype=torch.float16
        )  
        offload_directory = "../offload/"
        
        disk_offload(model=self._model, offload_dir=offload_directory)


        pipe = transformers.pipeline(
            "text-generation",
            model=model_id,
            device_map="auto",
        )

        print("Model download complete.")
        # this is to make sure, pipeline is loaded before we set model_loaded to True
        print(pipe("what is your name?"))
        
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
        global pipe
        result = pipe(prompt, **kwargs)
        return result[0]['generated_text']