from kafka import KafkaConsumer
import json
import requests
import os

TOPIC_NAME = 'locations'
KAFKA_SERVER = "{host}:{port}".format(host=os.getenv('KAFKA_SERVICE_HOST'), port=os.getenv('KAFKA_SERVICE_PORT'))
API_URL = "http://{host}:{port}/api/locations".format(host=os.getenv('UDACONNECT_API_SERVICE_HOST'),
                                                      port=os.getenv('UDACONNECT_API_SERVICE_PORT'))


def kafkaconsumer():
    try:
        consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER], consumer_timeout_ms=5000,
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    except Exception as err:
        return str(err)

    allresponse = ''
    for message in consumer:
        if all(key in message.value for key in ("creation_time", "longitude", "latitude", "person_id")):
            payload = json.dumps(message.value)
            headers = {'Content-type': 'application/json'}
            response = requests.post(API_URL, headers=headers, data=payload)
            data = response.json()
            allresponse += data
    if allresponse is '':
        return 'No messages found'
    else:
        return allresponse
