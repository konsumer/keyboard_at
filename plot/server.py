#!/usr/bin/env python3

"""Simple https server for development."""

import ssl
from http.server import HTTPServer, SimpleHTTPRequestHandler

CERTFILE = './localhost.pem'


def main():
    https_server(certfile=CERTFILE)


def https_server(*, certfile):
    print('`https_server()` starts...')
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERTFILE)

    server_address = ('', 443)
    with HTTPServer(server_address, SimpleHTTPRequestHandler) as httpd:
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print_server_info(httpd)
        try:
            httpd.serve_forever()
        except Exception as e:
            httpd.server_close()
            raise e


def print_server_info(server):
    print(f"https://{server.server_name}")


if __name__ == "__main__":
    main()