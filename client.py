import grpc
import hashlib
import hash_pb2
import hash_pb2_grpc
import os
import logging

from config import FE_SERVER_CERT

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def fill_with_deadbeef(idx, size):
    deadbeef = bytes.fromhex('AAAAAAAA')
    deadbeef = deadbeef[:-1] + bytes([idx % 256])
    repeated_value = deadbeef * (size // len(deadbeef))
    remaining_bytes = deadbeef[:size % len(deadbeef)]
    result = repeated_value + remaining_bytes

    return result

def generate_requests(num_requests, size):
    for i in range(num_requests):
        data = fill_with_deadbeef(i, size)
        logging.info(f'Sending request of size {len(data)} bytes. Expected hash: {hashlib.sha1(data).digest().hex()}')
        yield hash_pb2.HashRequest(data=data)

def run():
    with grpc.secure_channel('pepe.chimeratool.com:443', grpc.tls_channel_credentials(root_certificates=FE_SERVER_CERT, key_log_file_path="/home/pepe/.ssl-key-client.log")) as channel:
        stub = hash_pb2_grpc.HasherStub(channel)
        for response in stub.HashMe(generate_requests(100, 1024*1024)):
            logging.info(f"Recieved hash: {response.hash.hex()}")

if __name__ == '__main__':
    run()
