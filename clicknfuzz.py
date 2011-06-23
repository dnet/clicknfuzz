from SocketServer import *
from socket import *
import sys

class MyTCPHandler(BaseRequestHandler):

    def setup(self):
        self.sock_out=socket(AF_INET,SOCK_STREAM)
        self.sock_out.connect(('localhost',8888))
    
    def handle(self):
        while 1:
            self.data = self.request.recv(1024).strip()
            if not self.data: break
            self.sock_out.send(self.data)

    def finish(self):
        self.sock_out.close()

class ThreadingTCPServer(ThreadingMixIn, TCPServer): pass

if __name__ == "__main__":
    if len(sys.argv)<5:
        print "Usage: clicknfuzz.py listen_host listen_port target_host target_port"
    HOST, PORT = sys.argv[1], sys.argv[2]

    # Create the server, binding to localhost on port 9999
    server = ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
