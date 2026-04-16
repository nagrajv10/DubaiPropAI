FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY be/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# We run Docker build from root context to copy ML models
COPY ml/models /ml/models
ENV MODELS_PATH=/ml/models/models.joblib

COPY be/ /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
