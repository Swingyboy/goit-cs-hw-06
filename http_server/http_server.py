from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import os
import socket
from urllib.parse import urlparse


logging.basicConfig(level=logging.DEBUG)

HTTP_HOST = os.environ.get("HTTP_HOST", "localhost")
HTTP_PORT = int(os.environ.get("HTTP_PORT", 3000))
SOCKET_PORT = int(os.environ.get("SOCKET_PORT", 5000))
SOCKET_HOST = os.environ.get("SOCKET_HOST", "localhost")


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        super().__init__(*args, **kwargs)

    def _parse_path(self):
        url = urlparse(self.path)
        return url.path

    def _send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def _send_image_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "image/png")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def _send_style_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/css")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def do_GET(self):
        path = self._parse_path()
        if path == "/":
            self._send_html_file("pages/index.html")
        elif path == "/message.html":
            self._send_html_file("pages/message.html")
        elif path == "/logo.png":
            self._send_image_file("pages/logo.png")
        elif path == "/style.css":
            self._send_style_file("pages/style.css")
        else:
            self._send_html_file("pages/error.html", status=404)

    def do_POST(self):
        path = self._parse_path()
        if path == "/message":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            if post_data:
                try:
                    data = post_data.decode("utf-8")
                except UnicodeDecodeError:
                    self._send_html_file("pages/error.html", status=400)
                else:
                    logging.debug(f"Received data: {data}")
                try:
                    self.sock.sendto(data.encode("utf-8"), (SOCKET_HOST, SOCKET_PORT))
                except Exception as e:
                    logging.error(f"Error sending data: {e}")
                    self._send_html_file("pages/error.html", status=500)
                self._send_html_file("pages/success.html")

        else:
            self._send_html_file("pages/error.html", status=404)


class Server:
    def __init__(self, host: str = HTTP_HOST, port: int = HTTP_PORT):
        self.server = HTTPServer((host, port), RequestHandler)

    def run(self):
        self.server.serve_forever()


if __name__ == "__main__":
    server = Server()
    server.run()
