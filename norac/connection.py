#!/usr/bin/env python
import ssl
import socket
import json

class Connection:

    def init(self, config):
        self.buffer_size = config.getint("network", "buffersize")

        proto_str = config.get("security", "protocol")
        protocol = ssl.__dict__["PROTOCOL_" + proto_str]
        self.ssl_context = ssl.SSLContext(protocol)

        ciphers = config.get("security", "ciphers")
        self.ssl_context.set_ciphers(ciphers)

        cafile = config.get("security", "cafile")
        self.ssl_context.load_verify_locations(cafile)

        certificate = config.get("security", "certificate")
        key = config.get("security", "key")
        self.ssl_context.load_cert_chain(certificate, key)

        if config.getboolean("security", "verify"):
            self.ssl_context.verify_mode = ssl.CERT_REQUIRED
        else:
            self.ssl_context.verify_mode = ssl.CERT_NONE

        check_hostname = config.getboolean("security", "check_hostname")
        self.ssl_context.check_hostname = check_hostname

        self.server_name = config.get("security", "server_name")
        self.host = config.get("default", "ip")
        self.port = config.getint("default", "port")

    def send_request(self, request):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = self.ssl_context.wrap_socket(sock, server_hostname=self.server_name)

        ssl_sock.connect((self.host, self.port))

        request_txt = json.dumps(request) 
        
        sent = 0
        while sent < len(request_txt):
            sent += ssl_sock.send(request_txt[sent:])

        response_txt = ""
        received = self.buffer_size
        while received == self.buffer_size:
            tmp = ssl_sock.recv(self.buffer_size)
            response_txt += tmp
            received = len(tmp) 

        ssl_sock.close()

        response = json.loads(response_txt) 
        return response
