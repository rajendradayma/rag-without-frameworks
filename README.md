
***

# RAG Without Frameworks

A Retrieval-Augmented Generation (RAG) chatbot and document QA system featuring:
- **FastAPI backend** for PDF ingestion and language model querying.
- **Chainlit frontend** for interactive chat and document upload.
- **Dockerized setup** for easy deployment.
- **Secure** use of secrets via environment variables.

***

## Features

- Upload PDFs and query contents using a conversational frontend.
- FastAPI backend integrates Groq API and manages all retrieval logic.
- Chainlit provides an interactive UI with PDF upload and chat.
- Docker Compose deployment for both backend and frontend.
- Secrets (`.env` files) excluded from repository for safety.

***

## Getting Started

### Prerequisites

- Git
- Docker & Docker Compose

### Clone the repository

```bash
git clone https://github.com/your-username/rag-without-frameworks.git
cd rag-without-frameworks
```

### Project Structure

```
rag-without-frameworks/
│
├─ backend/           # FastAPI app and API logic
│   ├─ main.py
│   ├─ requirements.txt
│   └─ .env.example   # Use this template for your secrets
│
├─ frontend/          # Chainlit app and frontend logic
│   ├─ main.py
│   └─ Dockerfile
│
├─ docker-compose.yml # Compose file to run both services
├─ .gitignore         # Ensures .venv and secrets are not tracked
└─ README.md
```

### Set environment variables

- In `backend/`, copy `.env.example` to `.env` and fill with your Groq API key and preferred models.

### Build and Run with Docker

```bash
docker-compose build
docker-compose up -d
```

- Backend: http://localhost:8000
- Frontend (Chainlit UI): http://localhost:8501

***

## Usage

1. Access the Chainlit UI at [http://localhost:8501](http://localhost:8501).
2. Upload a PDF using the paperclip icon.
3. Ask your questions in natural language.
4. Retrieve results backed by your RAG pipeline.

***

## Security

- **Do not commit secrets.**  
  Your `.env` files are excluded via `.gitignore`.
- For configuration, share only `.env.example` (no real secrets).

***

## Contributing

Pull requests and issues are welcome! For major changes, open an issue first to discuss what you’d like to change.

***

## License

This project is distributed under the MIT License. See `LICENSE` for more information.


