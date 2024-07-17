from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse


class RequestHandler(BaseHTTPRequestHandler):
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
            self._send_html_file("./pages/index.html")
        elif path == "/message.html":
            self._send_html_file("./pages/message.html")
        elif path == "/logo.png":
            self._send_image_file("./pages/logo.png")
        elif path == "/style.css":
            self._send_style_file("./pages/style.css")
        else:
            self._send_html_file("./pages/error.html", status=404)

    def do_POST(self):
        path = self._parse_path()
        if path == "/message":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            with open("./pages/message.txt", "wb") as fd:
                fd.write(post_data)
            self._send_html_file("./pages/success.html")
        else:
            self._send_html_file("./pages/error.html", status=404)


class Server:
    def __init__(self, host="localhost", port=8000):
        self.server = HTTPServer((host, port), RequestHandler)

    def run(self):
        self.server.serve_forever()


if __name__ == "__main__":
    server = Server()
    server.run()
