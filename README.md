# Hash service

Minimal example of a service using bidirectional streaming with gRPC and Python. 

* `server.py` creates a secure channel with a self-signed certificate.
* `client.py` sends a message to the server and receives the hash of the message.


## Usage from Docker

Build the image with the following command:

```
$ docker build . -t grpc-hash-service:latst
```

Running the image **as a server**:

```
$ docker run --rm -it grpc-hash-service:latest
```

Running the image **as a client**:

```
docker run --rm -it grpc-hash-service:latest client.py
```

## Arguments of `client.py`

It possible to modify the number of requests and the size of a request via CLI argument of the `client.py`.

```
docker run --rm -it grpc-hash-service:latest client.py --num_requests 100 --size 1048576
```

(These are the default values above.)

Also there is a `--help` option for more details.
