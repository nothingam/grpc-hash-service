def read_file(path):
    with open(path, 'rb') as f:
        return f.read()

SERVER_CERT = read_file('./certs/server.crt') 
SERVER_KEY = read_file('./certs/server.key')