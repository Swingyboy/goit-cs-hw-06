from socket import socket, AF_INET, SOCK_DGRAM
import logging
import json

logging.basicConfig(level=logging.DEBUG)


class SocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def _parse_data(self, data: str) -> dict:
        content = dict()
        data = data.split("&")
        for i in data:
            key, value = i.split("=")
            content[key] = value
        return content

    def start(self):
        print(f"Listening on {self.host}:{self.port}")
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                data = data.decode("utf-8")
                data = self._parse_data(data)
                logging.debug(f"Received data: {data}")
            except KeyboardInterrupt:
                break
        logging.debug("Server stopped")
        self.sock.close()


if __name__ == "__main__":
    SOCKET_PORT = 5000
    SOCKET_HOST = "localhost"
    server = SocketServer(SOCKET_HOST, SOCKET_PORT)
    server.start()
