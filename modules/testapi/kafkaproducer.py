# This is a testing script to send a create location request to Kafka server

from kafka import KafkaProducer
import json
import datetime
import os

TOPIC_NAME = 'locations'
KAFKA_SERVER = "{host}:{port}".format(host=os.getenv('KAFKA_SERVICE_HOST'), port=os.getenv('KAFKA_SERVICE_PORT'))

locations = [
    {
        "creation_time": datetime.datetime.now().isoformat(),
        "longitude": "37.55363",
        "person_id": 5,
        "latitude": "-122.290883"
    }
]


def kafkaproducer():
    try:
        producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    except Exception as err:
        return str(err)

    for location in locations:
        producer.send(TOPIC_NAME, location)
    producer.flush()
    return "Message(s) sent to Kafka!"
