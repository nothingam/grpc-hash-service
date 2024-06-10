import grpc
import hash_pb2
import hash_pb2_grpc
import os
import logging

from config import FE_SERVER_CERT

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def generate_requests(num_requests, size):
    for _ in range(num_requests):
        data = os.urandom(size)
        logging.info(f'Sending request of size {len(data)} bytes.')
        yield hash_pb2.HashRequest(data=data)

def run():
    with grpc.secure_channel('localhost:50052', grpc.ssl_channel_credentials(root_certificates=FE_SERVER_CERT)) as channel:
        stub = hash_pb2_grpc.HasherStub(channel)
        for response in stub.HashMe(generate_requests(100, 1024*1024)):
            logging.info(f"Recieved hash: {response.hash.hex()}") 

if __name__ == '__main__':
    run()
