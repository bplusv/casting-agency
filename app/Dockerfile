FROM python:3.8.5-slim-buster

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN useradd -m appuser
USER appuser

CMD gunicorn --bind 0.0.0.0:$PORT app:app
