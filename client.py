import grpc
import hash_pb2
import hash_pb2_grpc
import os
import random

from config import FE_SERVER_CERT

def generate_requests(num_requests, size):
    for _ in range(num_requests):
        data = os.urandom(size)
        yield hash_pb2.HashRequest(data=data)

def run():
    with grpc.secure_channel('localhost:50052', grpc.ssl_channel_credentials(root_certificates=FE_SERVER_CERT)) as channel:
        stub = hash_pb2_grpc.HasherStub(channel)
        responses = stub.HashMe(generate_requests(100, 32768*2))
        for response in responses:
            print(f"Received hash: {response.hash.hex()}")

if __name__ == '__main__':
    run()
