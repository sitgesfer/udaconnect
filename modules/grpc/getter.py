# This is a tester script to send a connection request to the gGRPC server

import grpc
import connection_pb2
import connection_pb2_grpc

print("Sending test payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = connection_pb2_grpc.ConnectionServiceStub(channel)

response = stub.Get(connection_pb2.ConnectionRequest(
    person_id=1,
    start_date="2020-08-15",
    end_date="2020-08-16",
    distance=5
))
print(response)
