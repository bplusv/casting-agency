FROM python:3.8.6-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP="src.app:create_app()"
CMD flask db upgrade && gunicorn --bind 0.0.0.0:$PORT $FLASK_APP
