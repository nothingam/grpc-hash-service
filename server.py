import grpc
from concurrent import futures
import hash_pb2
import hash_pb2_grpc
import struct
import argparse

class HasherServicer(hash_pb2_grpc.HasherServicer):
    def HashMe(self, request_iterator, context):
        for request in request_iterator:
            first_word = struct.unpack('<I', request.data[0:4])[0]
            print(f'Received idx: {first_word}, sending response')
            yield hash_pb2.HashResponse(hash=first_word.to_bytes(4, 'little'))

def serve(port, server_key, server_cert):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hash_pb2_grpc.add_HasherServicer_to_server(HasherServicer(), server)
    server.add_secure_port(f'[::]:{port}', grpc.ssl_server_credentials([(server_key, server_cert)]))
    server.start()
    print(f'Server is up and running.')
    server.wait_for_termination()

if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Server for the hash service')
    args.add_argument('--port', type=int, default=50052, help='Port to listen on')
    args.add_argument('--server_key', type=str, default='./certs/server.key', help='Server key')
    args.add_argument('--server_cert', type=str, default='./certs/server.crt', help='Server crt')

    args = args.parse_args()

    def read_file(path):
        with open(path, 'rb') as f:
            return f.read()

    server_key =  read_file(args.server_key)
    server_cert = read_file(args.server_cert)

    serve(args.port, server_key, server_cert)
