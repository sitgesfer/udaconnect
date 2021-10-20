from kafka import KafkaConsumer
import json
import requests
import os
import logging

TOPIC_NAME = 'locations'
KAFKA_SERVER = "{host}:{port}".format(host=os.getenv('KAFKA_SERVICE_HOST'), port=os.getenv('KAFKA_SERVICE_PORT'))
API_URL = "http://{host}:{port}/api/locations".format(host=os.getenv('UDACONNECT_API_SERVICE_HOST'),
                                                      port=os.getenv('UDACONNECT_API_SERVICE_PORT'))


try:
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER], consumer_timeout_ms=5000,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    print('Kafka consumer started')
except Exception as err:
    print(str(err))
    exit()

root = logging.getLogger()
allresponse = ''
for message in consumer:
    print('Received message:')
    print(str(message.value))
    if all(key in message.value for key in ("creation_time", "longitude", "latitude", "person_id")):
        payload = json.dumps(message.value)
        headers = {'Content-type': 'application/json'}
        response = requests.post(API_URL, headers=headers, data=payload)
        data = response.json()
        allresponse = allresponse + str(data)
        print('Response from API:')
        print(str(data))
    else:
        print('Location message has an invalid format')
if allresponse == '':
    print('No messages found')
else:
    print(allresponse)
