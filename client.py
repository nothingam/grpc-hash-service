import grpc
import hash_pb2
import hash_pb2_grpc
import os
import random
import argparse

from config import FE_SERVER_CERT

def generate_requests(num_requests, size):
    for _ in range(num_requests):
        data = os.urandom(size)
        yield hash_pb2.HashRequest(data=data)

def run(num_requests, size):
    print("Sending %d requests of size %d bytes" % (num_requests, size))
    with grpc.secure_channel('pepe.chimeratool.com:443', grpc.ssl_channel_credentials(root_certificates=FE_SERVER_CERT)) as channel:
        stub = hash_pb2_grpc.HasherStub(channel)
        responses = stub.HashMe(generate_requests(num_requests, size))
        for response in responses:
            print(f"Received hash: {response.hash.hex()}")

if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Client for the hash service')
    args.add_argument('--num_requests', type=int, default=100, help='Number of requests to send')
    args.add_argument('--size', type=int, default=1024*1024, help='Size of each request in bytes')

    args = args.parse_args()

    run(args.num_requests, args.size)
