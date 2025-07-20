FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/db && chmod -R a+rwx /app/db

RUN pip install flask flask_sqlalchemy

COPY app/ .

CMD ["python", "app.py"]