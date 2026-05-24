FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir huggingface_hub

COPY download_bert_model.py .

RUN python download_bert_model.py

COPY . .

ENV HF_ENDPOINT=https://hf-mirror.com
ENV HF_HUB_ENABLE_HF_TRANSFER=0
ENV TRANSFORMERS_OFFLINE=1

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]