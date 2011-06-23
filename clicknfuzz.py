from threading import *
from socket import *
import sys

class ServerDispatcher:
    def __init__(self,listen_host,listen_port,target_host,target_port):
        self.listen_host=listen_host
        self.listen_port=listen_port
        self.target_host=target_host
        self.target_port=target_port
        
        self.server=None
        self.threads=[]

    def bind_socket(self):
        try:
            self.server=socket(AF_INET,SOCK_STREAM)
            self.server.bind((self.listen_host,self.listen_port))
            self.server.listen(5)
        except error, (value,message):
            if self.server:
                self.server.close()
            print "Could not start server: "+message
            sys.exit(1)

    def run(self):
        self.bind_socket()
        while 1:
            st=ServerThread(self.server.accept(),self.target_host,self.target_port)
            st.start()
            self.threads.append(st)

class ServerThread(Thread):
    def __init__(self,(client,address),target_host,target_port):
        super(ServerThread,self).__init__()
        self.client=client
        self.address=address
        self.target_host=target_host
        self.target_port=target_port
        self.sock_out=None

    def run(self):
        self.sock_out=socket(AF_INET,SOCK_STREAM)
        self.sock_out.connect((self.target_host,self.target_port))
        while 1:
            data=self.client.recv(1024)
            if data:
                print "Got: "+data
                self.sock_out.send(data)
            else:
                self.client.close()
                self.sock_out.close()
                break


if __name__ == "__main__":
    sd=ServerDispatcher("localhost",9999,"localhost",8888)
    sd.run()


