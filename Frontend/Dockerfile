FROM python:3.10-slim

WORKDIR /app

COPY frontend/ .

RUN pip install --upgrade pip
RUN pip install chainlit requests

EXPOSE 8501

CMD ["chainlit", "run", "main.py", "--host", "0.0.0.0", "--port", "8501"]
