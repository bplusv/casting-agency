FROM python:3.8.6-buster

WORKDIR /app
RUN useradd -m appuser
RUN chown appuser:appuser /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER appuser
COPY --chown=appuser:appuser . .

ENV FLASK_APP="src.main:create_app()"
CMD flask db upgrade && gunicorn --bind 0.0.0.0:$PORT $FLASK_APP
