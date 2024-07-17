from datetime import datetime
import logging
import os
import pymongo
from socket import socket, AF_INET, SOCK_DGRAM

logging.basicConfig(level=logging.DEBUG)

HOST = os.environ.get("SOCKET_HOST", "localhost")
PORT = int(os.environ.get("SOCKET_PORT", 5000))
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))


class SocketServer:
    def __init__(self, host: str = HOST, port: int = PORT, mongo_host: str = MONGO_HOST, mongo_port: int = MONGO_PORT):
        self.host: str = host
        self.port: int = port
        self.mongo_host: str = mongo_host
        self.mongo_port: int = mongo_port
        self.sock: socket = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.mongo_client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        self.db = self.mongo_client["web_app"]
        self.messages = self.db["messages"]

    def _parse_data(self, data: str) -> dict:
        content = dict()
        data = data.split("&")
        for i in data:
            key, value = i.split("=")
            content[key] = value
        content["date"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logging.debug(f"Parsed data: {content}")
        return content

    def start(self):
        print(f"Listening on {self.host}:{self.port}")
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                logging.debug(f"Received data: {data}")
                data = data.decode("utf-8")
                data = self._parse_data(data)
                logging.debug(f"Inserting data: {data}")
                self.messages.insert_one(data)
            except KeyboardInterrupt:
                break
        logging.debug("Server stopped")
        self.sock.close()


if __name__ == "__main__":
    server = SocketServer(HOST, PORT)
    server.start()
