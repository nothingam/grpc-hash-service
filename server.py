import grpc
from concurrent import futures
import hashlib
import hash_pb2
import hash_pb2_grpc
from config import SERVER_CERT, SERVER_KEY
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class HasherServicer(hash_pb2_grpc.HasherServicer):
    def HashMe(self, request_iterator, context):
        for request in request_iterator:
            logging.info(f'Received request of size {len(request.data)} bytes.')
            sha1_hash = hashlib.sha1(request.data).digest()
            logging.info(f'Sending response with hash {sha1_hash.hex()}.')
            yield hash_pb2.HashResponse(hash=sha1_hash)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hash_pb2_grpc.add_HasherServicer_to_server(HasherServicer(), server)
    server.add_secure_port('[::]:50052', grpc.ssl_server_credentials([(SERVER_KEY, SERVER_CERT)]))
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
