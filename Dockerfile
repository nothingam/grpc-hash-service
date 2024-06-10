FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir poetry

RUN poetry install && poetry run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. hash.proto

EXPOSE 50052

CMD ["poetry", "run", "python", "server.py"]
