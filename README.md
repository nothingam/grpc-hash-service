# Hash service

Minimal example of a service using bidirectional streaming with gRPC and Python.

* `server.py` creates a secure channel with a self-signed certificate.
* `client.py` sends a message to the server and receives the hash of the message.

## Usage from Docker


### Building the image

Build the image with the following command:

```
$ docker build . -t grpc-hash-service:latest
```

### Pulling from docker hub

You can pull the available image from docker hub:

```bash
$ docker pull nothingam/grpc-hash-service:latest
```

### Running the image

Running the image **as a client**:

```
$ docker run --rm -it grpc-hash-service:latest client.py
```

Starts the client, which connects to `pepe2.chimeratool.com` on port 443.

See `--help` for more details.

> NOTE: be aware that by using the default parameters the `client.py` is connecting to `pepe2.chimeratool.com:443` by using the certificate from `certs/fe-server.crt` (which is ponting to `certs/pepe2-chimeratool-com.pem`)

Running the image **as a server**:

```
$ docker run --rm -it grpc-hash-service:latest server.py
```

Starts the service, which listens on port 50052. The server uses the certificate from `certs/server.crt` and key from `certs/server.key` for SSL layer. Port, certificate and key can be modified via CLI argument (see `--help` for more details).


## Arguments of `client.py`

It possible to modify the number of requests and the size of a request via CLI argument of the `client.py`.

```
$ docker run --rm -it grpc-hash-service:latest client.py --num_requests 100 --size 1048576
```

(These are the default values above.)

Also there is a `--help` option for more details.

## Installing from source

Project uses `poetry` for dependency management. Install the dependencies with the following command:

```bash
$ git clone https://github.com/nothingam/grpc-hash-service.git
$ cd grpc-hash-service
$ poetry install
```

... after installation you can run the client with the following command:

```bash
$ poetry run python client.py
```

... or spawn a new shell with the following command:

```bash
$ poetry shell
```

More info on poetry: https://python-poetry.org/ .