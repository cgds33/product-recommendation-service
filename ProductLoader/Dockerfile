FROM python:3.8-slim

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY etl_worker.py .

CMD ["celery", "-A", "etl_worker:app", "worker", "--loglevel=info"]
