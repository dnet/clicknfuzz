from threading import *
from socket import *
import sys
import ConfigParser

class ServerDispatcher:
    def __init__(self,listen_host,listen_port,target_host,target_port,fuzzers):
        self.listen_host=listen_host
        self.listen_port=listen_port
        self.target_host=target_host
        self.target_port=target_port
        self.modules=fuzzers

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
            st=ServerThread(self.server.accept(),self.target_host,self.target_port,fuzzers)
            st.start()
            self.threads.append(st)

class ServerThread(Thread):
    def __init__(self,(client,address),target_host,target_port,fuzzers):
        super(ServerThread,self).__init__()
        self.client=client
        self.address=address
        self.target_host=target_host
        self.target_port=target_port
        self.fuzzers=fuzzers
        self.sock_out=None


    def run(self):
        self.sock_out=socket(AF_INET,SOCK_STREAM)
        self.sock_out.connect((self.target_host,self.target_port))
        while 1:
            data=self.client.recv(1024)
            if data:
                print "Got: "+data
                self.sock_out.send(data)
                answer=self.sock_out.recv(1024)
                self.client.send(answer)
                for fuzzer in self.fuzzers:
                    fuzzer.set_data(data)
                    for f in fuzzer:
                        self.sock_out.send(f)
            else:
                self.client.close()
                self.sock_out.close()
                break


def list_to_dict(l):
    d={}
    for li in l:
        d[li[0]]=li[1]

    return d

if __name__ == "__main__":
    if len(sys.argv)<2:
        print "Usage: clicknfuzz.py <configfile>"
        sys.exit(1)

    config=ConfigParser.RawConfigParser()
    config.read(sys.argv[1])

    sys.path.append("modules")
    module_names=config.sections()
    modules=map(__import__,module_names)
    fuzzers=[]
    for m in modules:
        f=m.Fuzzer(list_to_dict(config.items(m.__name__)))
        fuzzers.append(f)

    sd=ServerDispatcher(config.get('DEFAULT','listen_host'),config.getint('DEFAULT','listen_port'),
                        config.get('DEFAULT','target_host'),config.getint('DEFAULT','target_port'),fuzzers)
    sd.run()


