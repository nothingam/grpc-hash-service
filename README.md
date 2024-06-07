# Hash service

Minimal example of a service using bidirectional streaming with gRPC and Python. 

* `server.py` creates a secure channel with a self-signed certificate.
* `client.py` sends a message to the server and receives the hash of the message.
