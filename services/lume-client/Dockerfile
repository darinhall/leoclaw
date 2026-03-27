FROM python:3.11-slim

WORKDIR /app

COPY shared/ /app/shared/
COPY services/lume-client/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/lume-client/ /app/

ENV PYTHONPATH=/app
ENV MOCK_ACTIONS=true

CMD ["python", "client.py"]
