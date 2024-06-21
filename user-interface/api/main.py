from gevent import monkey

monkey.patch_all()

from endpoints import app, server_socket

if __name__ == "__main__":
    server_socket.run(app, debug=True, host="0.0.0.0", port=8000)
