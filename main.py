import configparser
from typing import Union
import lib
from lib.log import LogInfo
import player
from aiwolf_nlp_common import Action

def main(sock:Union[lib.connection.TCPServer,lib.connection.TCPClient], inifile:configparser.ConfigParser, received:list, name:str, log_info:LogInfo):
    agent = player.agent.Agent(inifile=inifile,name=name,log_info=log_info)
    if received != None: agent.set_received(received=received)

    while agent.gameContinue:

        if len(agent.received) == 0:
            agent.parse_info(receive=sock.receive())
        
        agent.get_info()
        message = agent.action()

        if Action.is_initialize(request=agent.request):
            agent = lib.util.init_role(agent=agent,inifile=inifile, name=name, log_info=log_info)

        if message != "":
            sock.send(message=message)

    return agent.received if len(agent.received) != 0 else None

if __name__ == "__main__":
    config_path = "./res/config.ini"

    inifile = lib.util.check_config(config_path=config_path)
    inifile.read(config_path,"UTF-8")

    while True:
    
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

        if not inifile.getboolean("connection","keep_connection"):
            break
