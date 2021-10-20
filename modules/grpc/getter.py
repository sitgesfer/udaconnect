# This is a tester script to send a connection request to the gGRPC server

import grpc
import connection_pb2
import connection_pb2_grpc
import os

print("Sending test payload...")

grpcport = os.getenv('UDACONNECT_GRPC_SERVICE_PORT')
channel = grpc.insecure_channel("localhost:{grpcport}".format(grpcport = grpcport))
stub = connection_pb2_grpc.ConnectionServiceStub(channel)

response = stub.Get(connection_pb2.ConnectionRequest(
    person_id=1,
    start_date="2020-08-15",
    end_date="2020-08-16",
    distance=5
))
print(response)
