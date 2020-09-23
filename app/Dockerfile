FROM python:3.8.5-buster
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m appuser
USER appuser

COPY --chown=appuser:appuser . .
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
