import grpc
import hash_pb2
import hash_pb2_grpc
import argparse


def generate_requests(num_requests, size):
    for idx in range(num_requests):
        print(f"Generating request {idx}")
        byte_data = idx.to_bytes(4, 'little')
        data = byte_data * (size // 4)
        yield hash_pb2.HashRequest(data=data)

def run(num_requests, size, host, port, server_cert):
    print("Sending %d requests of size %d bytes" % (num_requests, size))
    with grpc.secure_channel(f'{host}:{port}', grpc.ssl_channel_credentials(root_certificates=server_cert)) as channel:
        stub = hash_pb2_grpc.HasherStub(channel)
        responses = stub.HashMe(generate_requests(num_requests, size))
        for response in responses:
            idx = int.from_bytes(response.hash, 'little')
            print(f"Received idx: {idx}")

if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Client for the hash service')
    args.add_argument('--host', type=str, default='pepe2.chimeratool.com', help='Host to connect to')
    args.add_argument('--port', type=int, default=443, help='Host to connect to')
    args.add_argument('--num_requests', type=int, default=100, help='Number of requests to send')
    args.add_argument('--size', type=int, default=1024*1024, help='Size of each request in bytes')
    args.add_argument('--server_cert', type=str, default='./certs/fe-server.crt', help='Server crt')

    args = args.parse_args()

    with open(args.server_cert, 'rb') as f:
        server_cert = f.read()

    if (args.size % 4) != 0:
        print("Size must be a multiple of 4")
        exit(1)

    run(args.num_requests, args.size, args.host, args.port,  server_cert)
