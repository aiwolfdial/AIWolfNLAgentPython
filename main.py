import configparser
from typing import Union
import lib
import player
from lib.AIWolf.commands import AIWolfCommand

def main(sock:Union[lib.connection.TCPServer,lib.connection.TCPClient], inifile:configparser.ConfigParser, received:list, name:str):
    agent = player.agent.Agent(inifile=inifile,name=name)
    if received != None: agent.set_received(received=received)

    while agent.gameContinue:

        if len(agent.received) == 0:
            agent.parse_info(receive=sock.receive())
        
        agent.get_info()
        message = agent.action()

        if AIWolfCommand.is_initialize(request=agent.request):
            agent = lib.util.init_role(agent=agent,inifile=inifile, name=name)

        if message != "":
            sock.send(message=message)

    return agent.received if len(agent.received) != 0 else None

if __name__ == "__main__":
    config_path = "./res/config.ini"

    inifile = lib.util.check_config(config_path=config_path)
    inifile.read(config_path,"UTF-8")

    while inifile.getboolean("connection","keep_connection"):
    
        # connect to server or listen client
        if inifile.getboolean("connection","ssh_flag"):
            sock = lib.connection.SSHServer(inifile=inifile, name=inifile.get("agent","name1"))
        else:
            sock = lib.connection.TCPServer(inifile=inifile, name=inifile.get("agent","name1")) if inifile.getboolean("connection","host_flag") else lib.connection.TCPClient(inifile=inifile)
        
        sock.connect()

        received = None
        
        for _ in range(inifile.getint("game","num")):
            received = main(sock=sock, inifile=inifile, received=received, name=inifile.get("agent","name1"))
        
        sock.close()
