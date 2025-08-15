FROM python:3.11-slim
WORKDIR /app
COPY services/shared /app/services/shared
ENV PYTHONPATH=/app/services/shared
COPY services/api-gateway/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY services/api-gateway/app /app/app
ENV PORT=8080
CMD ["bash","-lc","uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
