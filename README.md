# langchain-llama-graph-server

A simple Flask API that serves a transformer model for text generation using Hugging Face's Transformers library. The application supports endpoints for loading the model and generating text based on user input.

## Features

- Load transformer models on demand.
- Generate text based on user-provided prompts.
- Built with Flask and Docker for easy deployment.

## Prerequisites

- Docker installed on your machine.
- Basic understanding of Docker and Flask.

## Project Structure

```
/your-project-directory
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env              # Environment variables
└── app
    └── main.py                 # Flask application code
    └── langchain_wrapper.py
    └── llm_providers
        └── base.py
        └── llama_provider.py
        └── openai_provider.py
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/jayahariv/langchain-llama-graph-server.git
   cd langchain-llama-graph-server
   ```

2. Create a `.env` file in the root directory if you need to set any environment variables.
    ```
    LANGCHAIN_API_KEY=<AddTokenHere>
    OPENAI_API_KEY=<AddTokenHere>
    LANGCHAIN_TRACING_V2=true
    USER_AGENT="agent-name"
    HUGGINGFACE_TOKEN=<AddTokenHere>
    ```

3. Edit the `requirements.txt` file to include any additional dependencies you may need.

## Docker Setup

### Build & Run the Docker Image

To build & run the Docker image, run the following command:

```bash
docker compose up --build -d
```

### Stop Docker Container

If you want to stop the containers running:

```bash
docker compose down
```

The application will be accessible at `http://localhost:8000`.

## API Endpoints

### 1. Start Loading the Model

- **Endpoint**: `/start-loading`
- **Method**: `POST`
- **Description**: Initiates the loading of the transformer model.

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

### 2. Check Loading Status

- **Endpoint**: `/loading-status`
- **Method**: `POST`
- **Description**: Checks the loading status of the model.

**Request**:
```bash
curl -X POST http://localhost:8000/loading-status -H "Content-Type: application/json" -d '{"provider": "llama"}'
```

**Response**:
```json
{
    "status": "loading" // or "loaded" or "not started"
}
```

### 3. Generate Text

- **Endpoint**: `/query`
- **Method**: `POST`
- **Description**: Generates text based on the provided prompt.

**Request**:
```bash
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"prompt": "Once upon a time..."}'
```

**Response**:
```json
{
    "result": "This is the generated text based on your prompt."
}
```

## Troubleshooting

- Ensure that your Docker container is running and accessible at `http://localhost:8000`.
- Check the logs for any error messages if the application does not behave as expected.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Notes

- Replace any placeholders such as repository URLs or usernames with your actual information.
- Adjust the content as necessary to fit the specific features and setup of your application.
- If you have any specific environment variables or configurations, make sure to document those in the README as well.

Feel free to modify this README to better fit your needs or to add additional sections if necessary!