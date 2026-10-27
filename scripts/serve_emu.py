#!/usr/bin/env python3
import os
import sys
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler

class EmuHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "build", "emu"))
        super().__init__(*args, directory=directory, **kwargs)

    def end_headers(self):
        # Enable SharedArrayBuffer and cross-origin isolation if required
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

def find_free_port(preferred_port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('127.0.0.1', preferred_port)) != 0:
            return preferred_port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else find_free_port(8000)
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, EmuHandler)
    url = f"http://localhost:{port}"
    print(f"=== Celery Man Web Emulator Server Running ===")
    print(f"Serving: {os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'build', 'emu'))}")
    print(f"URL: {url}")
    print(f"===============================================", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
