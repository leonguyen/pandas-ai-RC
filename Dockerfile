# Use Python 3.11
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git && rm -rf /var/lib/apt/lists/*
COPY . /app
RUN pip install --upgrade pip
RUN pip install pandasai pandasai-litellm pandas fastapi uvicorn[standard] python-multipart
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
