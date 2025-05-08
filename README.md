# LangChain-LLaMA-Graph-Server

A Flask-based API that leverages LangGraph to intelligently route text queries to either a LLaMA or OpenAI provider based on content type. Code-related queries are directed to LLaMA, while others go to OpenAI, with LLaMA follow-ups rerouted to OpenAI. The application is containerized with Docker for seamless deployment.

## Features

- **Dynamic Query Routing**: Uses LangGraph to route code-related queries to LLaMA and others to OpenAI.
- **Follow-Up Handling**: Redirects LLaMA follow-up queries to OpenAI.
- **Scalable Flask API**: Exposes endpoints for query processing and model management.
- **Dockerized Deployment**: Simplifies setup and scaling with Docker and Docker Compose.
- **Modular Design**: Extensible provider architecture for easy integration of additional LLMs.

## Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed.
- Basic familiarity with Flask, Python, and Docker.
- API keys for LLaMA (e.g., via Hugging Face) and OpenAI if using real providers.

## Project Structure

```
langchain-llama-graph-server/
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── app/
    ├── main.py             # Flask application
    ├── langchain_wrapper.py # LangGraph and LLM logic
    └── llm_providers/
        ├── base.py         # Base LLM provider class
        ├── llama_provider.py # LLaMA provider implementation
        └── openai_provider.py # OpenAI provider implementation
```

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jayahariv/langchain-llama-graph-server.git
   cd langchain-llama-graph-server
   ```

2. **Set Up Environment Variables**:
   Create a `.env` file in the root directory with the following:
   ```
   LANGCHAIN_API_KEY=<your-langchain-key>
   OPENAI_API_KEY=<your-openai-key>
   HUGGINGFACE_TOKEN=<your-huggingface-token>
   LANGCHAIN_TRACING_V2=true
   USER_AGENT="langchain-llama-graph-server"
   ```

3. **Install Dependencies**:
   Ensure `requirements.txt` includes:
   ```
   flask==2.3.3
   langgraph==0.2.5
   python-dotenv==1.0.1
   ```
   Add any additional dependencies (e.g., `openai`, `transformers`) as needed.

## Running with Docker

1. **Build and Run**:
   ```bash
   docker-compose up --build -d
   ```
   The API will be available at `http://localhost:8000`.

2. **Stop the Containers**:
   ```bash
   docker-compose down
   ```

## API Endpoints

### 1. Query Processing
- **Endpoint**: `/query`
- **Method**: `POST`
- **Description**: Processes a text query, routing it to LLaMA (code-related) or OpenAI (other queries).

**Request**:
```bash
curl -X POST http://localhost:8000/query \
-H "Content-Type: application/json" \
-d '{"query": "Write a Python function"}'
```

**Response**:
```json
{
    "query": "Write a Python function",
    "response": "OpenAI response for query: Write a Python function",
    "is_code_related": true,
    "from_llama": false
}
```

### 2. Start Model Loading
- **Endpoint**: `/start-loading`
- **Method**: `POST`
- **Description**: Initiates loading of LLM providers. This is not required now, 'query' API itself does the same loading checking and loads if not loaded earlier.

**Request**:
```bash
curl -X POST http://localhost:8000/start-loading
```

**Response**:
```json
{
    "message": "Model loading started."
}
```

### 3. Check Loading Status
- **Endpoint**: `/loading-status`
- **Method**: `POST`
- **Description**: Checks the loading status of a specified provider.

**Request**:
```bash
curl -X POST http://localhost:8000/loading-status \
-H "Content-Type: application/json" \
-d '{"provider": "llama"}'
```

**Response**:
```json
{
    "status": "loaded"
}
```

## Troubleshooting

- **API Unreachable**: Verify the Docker container is running (`docker ps`) and the port `8000` is accessible.
- **Model Loading Errors**: Check Docker logs (`docker-compose logs`) for issues with API keys or dependencies.
- **Invalid Responses**: Ensure the query JSON is correctly formatted and API keys are valid.

## Contributing

We welcome contributions! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please include tests and update documentation as needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.