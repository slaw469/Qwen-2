# Qwen2 API Server

A FastAPI server that provides OpenAI-compatible chat completions using the Qwen2-1.5B-Instruct model.

## Features

- OpenAI-compatible API endpoint (`/v1/chat/completions`)
- Qwen2-1.5B-Instruct model with 16-bit precision
- Health check endpoint
- Docker containerization for easy deployment

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Docker Deployment

1. Build the image:
```bash
docker build -t qwen2-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 qwen2-api
```

## API Usage

### Chat Completions

Send a POST request to `/v1/chat/completions`:

```json
{
  "model": "qwen2-1.5b-instruct",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "temperature": 0.2,
  "max_tokens": 150
}
```

### Health Check

GET `/health` returns the server status.

## Cloud Deployment

This repository is ready for deployment on platforms like:
- Railway
- Render
- Google Cloud Run
- AWS ECS
- Azure Container Instances

Simply connect your GitHub repository to your preferred cloud platform and deploy! 