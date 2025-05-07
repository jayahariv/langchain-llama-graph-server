from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv

load_dotenv()

from .llm_providers import get_providers  # noqa: E402
from .lanchain_wrapper import CustomLangChainLLM  # noqa: E402

app = Flask(__name__)
providers = get_providers()

# Global variables to manage model loading state
model_loading = False
model_loaded = False

# Placeholder for the model and tokenizer
model = None
tokenizer = None

# Index route
@app.route("/", methods=["GET"])
def index():
    return render_template_string('''
        <h1>API Documentation</h1>
        <p>Welcome to the LLM API!</p>
        <h2>Available Endpoints:</h2>
        <ul>
            <li><strong>GET /</strong>: Displays this documentation.</li>
            <li><strong>POST /query</strong>: Queries an LLM provider.</li>
        </ul>
        <h2>Usage Example</h2>
        <pre>
        curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{
          "provider": "openai_provider",
          "prompt": "What is the capital of France?"
        }'
        </pre>
    ''')

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    provider_name = data.get("provider")
    prompt = data.get("prompt")
    if provider_name not in providers:
        return jsonify({"error": "Unknown provider"}), 400

    llm = CustomLangChainLLM(provider=providers[provider_name])
    
    # customise here... for any further chaining and fine tuning. 

    result = llm.query(prompt)

    print(f"Querying {provider_name} with prompt: {prompt}")
    print(f"Result: {result}")
    return jsonify({"result": result})

@app.route("/start-loading", methods=["POST"])
def start_loading():
    data = request.json
    provider_name = data.get("provider")
    if provider_name not in providers:
        return jsonify({"error": "Unknown provider"}), 400
    
    return providers[provider_name].start_loading()

@app.route("/loading-status", methods=["POST"])
def loading_status():
    data = request.json
    provider_name = data.get("provider")    
    if provider_name not in providers:
        return jsonify({"error": "Unknown provider"}), 400
    
    return providers[provider_name].get_loading_status()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

