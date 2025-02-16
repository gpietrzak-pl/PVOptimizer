FROM python:3.9-slim-buster

WORKDIR /pvoptimizer

COPY pvoptimizer /pvoptimizer
COPY run.sh /

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt


CMD ["/run.sh"]