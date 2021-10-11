FROM debian:latest

WORKDIR /flaskapp
COPY requirements.txt .
COPY app.py .
COPY kafkaconsumer.py .
COPY kafkaproducer.py .
RUN apt-get update
RUN apt-get -y install python3 python3-venv python3-pip
RUN pip install -r requirements.txt
RUN pip install Flask

EXPOSE 5000

CMD ["flask", "run"]