FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install dash pandas redis

CMD ["python3", "dashboard.py"]