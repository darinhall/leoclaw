FROM python:3.11-slim

WORKDIR /app

COPY shared/ /app/shared/
COPY services/worker/ /app/

RUN pip install --no-cache-dir pydantic>=2.7.0

ENV PYTHONPATH=/app

CMD ["python", "worker.py"]
