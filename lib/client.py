import socket
from lib import(
    util
)

class Client:

    def __init__(self, config_path:str) -> None:
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        inifile = util.check_config(config_path=config_path)
        inifile.read(config_path,"UTF-8")
        self.host = inifile.get("connection","host")
        self.port = int(inifile.get("connection","port"))
        self.buffer = int(inifile.get("connection","buffer"))

    def connet(self) -> None:
        self.socket.connect((self.host,self.port))
    
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