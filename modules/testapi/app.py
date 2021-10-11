from flask import Flask
from kafkaconsumer import kafkaconsumer
from kafkaproducer import kafkaproducer

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Test API ready</p>"


@app.route("/consumer")
def showkafkaconsumer():
    return kafkaconsumer()


@app.route("/producer")
def runkarkaproducer():
    return kafkaproducer()
