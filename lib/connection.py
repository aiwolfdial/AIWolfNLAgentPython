import os
import socket
import paramiko
import configparser
from lib import(
    util
)

class Connection:
    def __init__(self,inifile:configparser.ConfigParser) -> None:
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.buffer = inifile.getint("connection","buffer")
    
    def receive(self, socket:socket.socket) -> str:
        responses = b""

        while not util.is_json_complate(responces=responses):
            response = socket.recv(self.buffer)
            
            if response == b"":
                raise RuntimeError("socket connection broken")
            
            responses += response

        return responses.decode("utf-8")
    
    def send(self, socket:socket.socket, message:str) -> None:
        message += "\n"

        socket.send(message.encode("utf-8"))
    
    def close(self) -> None:
        self.socket.close()

class TCPClient(Connection):

    def __init__(self, inifile:configparser.ConfigParser) -> None:
        super().__init__(inifile=inifile)
        self.host = inifile.get("tcp-client","host")
        self.port = inifile.getint("tcp-client","port")

    def connect(self) -> None:
        self.socket.connect((self.host,self.port))
    
    def receive(self) -> str:
        return super().receive(socket=self.socket)
    
    def send(self, message:str) -> None:
        super().send(socket=self.socket, message=message)

    def close(self) -> None:
        super().close()

class TCPServer(Connection):
    
    def __init__(self, inifile:configparser.ConfigParser, name:str) -> None:
        super().__init__(inifile=inifile)
        self.host_ip = inifile.get("tcp-server","ip")
        self.host_port = self.get_host_port(inifile=inifile, name=name)
        self.socket.bind((self.host_ip,self.host_port))
    
    def get_host_port(self, inifile:configparser.ConfigParser, name:str) -> int:

        if name == inifile.get("agent","name1"):
            return inifile.getint("tcp-server","port1")
        elif name == inifile.get("agent","name2"):
            return inifile.getint("tcp-server","port2")
        elif name == inifile.get("agent","name3"):
            return inifile.getint("tcp-server","port3")
        elif name == inifile.get("agent","name4"):
            return inifile.getint("tcp-server","port4")
        elif name == inifile.get("agent","name5"):
            return inifile.getint("tcp-server","port5")
        
        return None
    
    def connect(self):
        print("server listening...",end="\t")
        print("ip:" + self.host_ip + " port:" + str(self.host_port))
        self.socket.listen()
        self.client_socket, self.address = self.socket.accept()
    
    def receive(self) -> str:
        return super().receive(self.client_socket)
    
    def send(self, message: str) -> None:
        return super().send(socket=self.client_socket,message=message)
    
    def close(self):
        self.client_socket.close()
        super().close()


class SSHServer(Connection):
    def __init__(self,inifile:configparser.ConfigParser, name:str) -> None:
        super().__init__(inifile=inifile)
        self.ssh_config_path = inifile.get("ssh-server","config_path")
        self.ssh_host_name = inifile.get("ssh-server","host_name")
        self.ssh_agent_flag = inifile.getboolean("ssh-server","ssh_agent_flag")
        self.timeout = inifile.getint("ssh-server","timeout")
        self.ssh_remoteforward_port = self.get_ssh_port(inifile=inifile, name=name)

    def get_ssh_port(self, inifile:configparser.ConfigParser, name:str) -> int:
        if name == inifile.get("agent","name1"):
            return 0
        elif name == inifile.get("agent","name2"):
            return 1
        elif name == inifile.get("agent","name3"):
            return 2
        elif name == inifile.get("agent","name4"):
            return 3
        elif name == inifile.get("agent","name5"):
            return 4
    
    def read_ssh_config(self) -> paramiko.SSHConfigDict:
        config_file = os.path.expanduser(self.ssh_config_path)
        ssh_config = paramiko.SSHConfig()
        ssh_config.parse(open(config_file, 'r'))

        return ssh_config.lookup(self.ssh_host_name)
    
    def set_ssh_toolkit(self) -> None:
        self.ssh_client = paramiko.SSHClient()
        self.ssh_agent = paramiko.Agent()
        self.ssh_agent_keys = self.ssh_agent.get_keys()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    def set_ssh_config(self) -> None:
        self.config = self.read_ssh_config()
        self.ssh_pkey = None
        self.key_filename = None
        
        if self.ssh_agent_flag and len(self.ssh_agent_keys) > 0:
            self.ssh_pkey = self.ssh_agent_keys[0]
        elif self.ssh_agent_flag and len(self.ssh_agent_keys) == 0:
            raise ValueError("SSH agent does not contain any keys or the agent is not running.")
    
    def connect(self, remote_foward_flag = True) -> None:
        self.set_ssh_toolkit()
        self.set_ssh_config()
        
        self.ssh_client.connect(self.config["hostname"], username=self.config["user"], pkey=self.ssh_pkey, key_filename=self.config.get("identityfile"), timeout=self.timeout)

        if remote_foward_flag:
            self.ssh_remote_forward()
    
    def ssh_remote_forward(self) -> None:
        self.transport = self.ssh_client.get_transport()
        parts = self.config["remoteforward"][self.ssh_remoteforward_port].split()
        remote_port = int(parts[0])
        local_port = int(parts[1].split(":")[1])

        self.transport.request_port_forward(address="",port=remote_port)
        self.channel = self.transport.accept()
    
    def receive(self) -> str:
        return super().receive(self.channel)
    
    def send(self, message: str) -> None:
        print(message)
        return super().send(self.channel, message)
    
    def ssh_close(self) -> None:
        self.ssh_client.close()
    
    def close(self) -> None:
        self.ssh_close()
        return super().close()
