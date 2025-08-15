FROM python:3.11-slim
WORKDIR /app

# Shared lib
COPY services/shared /app/services/shared
ENV PYTHONPATH=/app/services/shared

# Deps
COPY services/pricing-svc/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# App
COPY services/pricing-svc/app /app/app

# Esegue il task in base a RUN_MODE:
# - RUN_MODE=loop       → ciclo continuo (worker)
# - RUN_MODE=recompute  → una singola riconfigurazione baseline (cron)
# - RUN_MODE=detect     → una singola passata di rilevazione deal
# Se non impostata, default = loop
CMD ["bash", "-lc", "python -m app.tasks ${RUN_MODE:-loop}"]
