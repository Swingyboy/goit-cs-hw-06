# Web Application with HTTP Server, Socket Server, and MongoDB

This project includes an HTTP server, a socket server, and a MongoDB database, all running as Docker services.
By default, the HTTP server listens on port 3000, the socket server listens on port 5000, and the MongoDB server listens on port 27017.

## Directory Structure
```
project/
├── docker-compose.yml
├── http_server/
│ ├── Dockerfile
│ ├── requirements.txt
│ ├── server.py
│ └── pages/
│ ├── index.html
│ ├── message.html
│ ├── logo.png
│ ├── style.css
│ ├── error.html
│ └── success.html
├── socket_server/
│ ├── Dockerfile
│ ├── requirements.txt
│ └── socket_server.py
```

## Prerequisites
- Docker
- Docker Compose
- Python 3

## Dependencies
- PyMongo

## Installation
1. Clone the repository
2. `cd` into the project directory
3. Run `docker-compose up` in the project directory

## Usage
1. Open a web browser and navigate to `http://localhost:3000`
2. Enter a message and click the "Send" button

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```