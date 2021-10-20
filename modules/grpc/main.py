import sys
import time
import requests
from concurrent import futures
import traceback
import json
import grpc
import connection_pb2
import connection_pb2_grpc
import os

API_URL = "http://{host}:{port}/api/persons/".format(host=os.getenv('UDACONNECT_API_SERVICE_HOST'),
                                                      port=os.getenv('UDACONNECT_API_SERVICE_PORT'))
API_URL = API_URL + '{person_id}/connection'


class ConnectionServicer(connection_pb2_grpc.ConnectionServiceServicer):
    def Get(self, request, context):
        headers = {'Content-type': 'application/json'}
        params = {
            "start_date": request.start_date,
            "end_date": request.end_date,
            "distance": request.distance
        }
        finalurl = API_URL.format(person_id=request.person_id)
        response = requests.get(finalurl, headers=headers, params=params)
        try:
            connections = json.loads(response.text)
            print(connections)
            result = connection_pb2.ConnectionMessageList()
            for connection in connections:
                msg_connection = connection_pb2.ConnectionMessage()
                msg_connection.person.id = connection['person']['id']
                msg_connection.person.company_name = connection['person']['company_name']
                msg_connection.person.last_name = connection['person']['last_name']
                msg_connection.person.first_name = connection['person']['first_name']
                msg_connection.location.id = connection['location']['id']
                msg_connection.location.person_id = connection['location']['person_id']
                msg_connection.location.creation_time = connection['location']['creation_time']
                msg_connection.location.longitude = connection['location']['longitude']
                msg_connection.location.latitude = connection['location']['latitude']
                result.connections.extend([msg_connection])
            return result
        except Exception:
            traceback.print_exc(file=sys.stdout)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
connection_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionServicer(), server)

grpcport = os.getenv('UDACONNECT_GRPC_SERVICE_PORT')
print("Server starting on port {grpcport}".format(grpcport = grpcport))
server.add_insecure_port("[::]:{grpcport}".format(grpcport = grpcport))
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
