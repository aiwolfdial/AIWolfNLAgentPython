import socket
import requests
import configparser
from lib import(
    util
)

class Connection:
    def __init__(self,inifile:configparser.ConfigParser) -> None:
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.buffer = inifile.getint("connection","buffer")
    
    def receive(self) -> str:
        responses = b""

        while not util.is_json_complate(responces=responses):
            response = self.socket.recv(self.buffer)
            
            if response == b"":
                raise RuntimeError("socket connection broken")
            
            responses += response

        return responses.decode("utf-8")
    
    def send(self, message:str) -> None:
        message += "\n"

        self.socket.send(message.encode("utf-8"))
    
    def close(self) -> None:
        self.socket.close()

class Client(Connection):

    def __init__(self, inifile:configparser.ConfigParser) -> None:
        super().__init__(inifile=inifile)
        self.host = inifile.get("connection-client","host")
        self.port = inifile.getint("connection-client","port")

    def connect(self) -> None:
        self.socket.connect((self.host,self.port))
    
    def receive(self) -> str:
        return super().receive()
    
    def send(self, message:str) -> None:
        super().send(message=message)

    def close(self) -> None:
        super().close()

class Server(Connection):
    
    def __init__(self, inifile:configparser.ConfigParser, name:str) -> None:
        super().__init__(inifile=inifile)
        self.gip = self.get_gip_addr()
        self.host_port = self.get_host_port(inifile=inifile, name=name)
        self.socket.bind((self.gip,self.host_port))
    
    def get_host_port(self, inifile:configparser.ConfigParser, name:str) -> int:

        if name == inifile.get("agent","name1"):
            return inifile.getint("connection-server","port1")
        elif name == inifile.get("agent","name2"):
            return inifile.getint("connection-server","port2")
        elif name == inifile.get("agent","name3"):
            return inifile.getint("connection-server","port3")
        elif name == inifile.get("agent","name4"):
            return inifile.getint("connection-server","port4")
        elif name == inifile.get("agent","name5"):
            return inifile.getint("connection-server","port5")
        
        return None
    
    def get_gip_addr(self):
        res = requests.get('https://ifconfig.me')
        return res.text
    
    def connect(self):
        print("server listening...")
        print("ip: " + self.gip)
        print("port: " + str(self.host_port))
        self.socket.listen()
        self.socket.accept()
    
    def receive(self) -> str:
        return super().receive()
    
    def send(self, message: str) -> None:
        return super().send(message)
    
    def close(self):
        super().close()