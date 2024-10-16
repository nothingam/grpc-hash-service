import grpc
from concurrent import futures
import hashlib
import hash_pb2
import hash_pb2_grpc
from config import SERVER_CERT, SERVER_KEY
import struct

class HasherServicer(hash_pb2_grpc.HasherServicer):
    def HashMe(self, request_iterator, context):
        for request in request_iterator:
            first_word = struct.unpack('<I', request.data[0:4])[0]
            print(f'Received idx: {first_word}, sending response')
            yield hash_pb2.HashResponse(hash=first_word.to_bytes(4, 'little'))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hash_pb2_grpc.add_HasherServicer_to_server(HasherServicer(), server)
    server.add_secure_port('[::]:50052', grpc.ssl_server_credentials([(SERVER_KEY, SERVER_CERT)]))
    server.start()
    print(f'Server is up and running.')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
