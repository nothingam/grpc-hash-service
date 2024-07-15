import grpc
from concurrent import futures
import hashlib
import hash_pb2
import hash_pb2_grpc
from config import SERVER_CERT, SERVER_KEY

class HasherServicer(hash_pb2_grpc.HasherServicer):
    def HashMe(self, request_iterator, context):
        for request in request_iterator:
            print(f'Received request of size {len(request.data)} bytes.')
            sha1_hash = hashlib.sha1(request.data).digest()
            yield hash_pb2.HashResponse(hash=sha1_hash)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hash_pb2_grpc.add_HasherServicer_to_server(HasherServicer(), server)
    server.add_secure_port('[::]:50052', grpc.ssl_server_credentials([(SERVER_KEY, SERVER_CERT)]))
    server.start()
    print(f'Server is up and running.')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
