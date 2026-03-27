FROM python:3.11-slim

WORKDIR /app

# Install shared library first (layer-cached)
COPY shared/ /app/shared/
COPY services/orchestrator/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/orchestrator/app/ /app/app/

ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
