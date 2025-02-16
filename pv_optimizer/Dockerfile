FROM python:3.9-slim-buster

WORKDIR /app

COPY pv_optimizer /app/pv_optimizer
COPY run.sh /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt


CMD ["/app/run.sh"]