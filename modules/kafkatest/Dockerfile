FROM python:latest

WORKDIR /kafkatest
COPY requirements.txt .
COPY kafkaconsumer.py .
COPY kafkaproducer.py .
RUN pip install -r requirements.txt

CMD ["python3", "kafkaconsumer.py"]