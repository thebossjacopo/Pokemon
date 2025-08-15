FROM python:3.11-slim
WORKDIR /app
COPY services/shared /app/services/shared
ENV PYTHONPATH=/app/services/shared
COPY services/pricing-svc/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY services/pricing-svc/app /app/app
CMD ["bash", "-lc", "python -m app.tasks loop"]
