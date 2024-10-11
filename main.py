import configparser
from typing import Union
import lib
from lib.log import LogInfo
import player
from aiwolf_nlp_common import util
from aiwolf_nlp_common import Action
from aiwolf_nlp_common.connection import Connection
from aiwolf_nlp_common.connection.tcp import(
    TCPClient,
    TCPServer
)
from aiwolf_nlp_common.connection.ssh import SSHServer
from aiwolf_nlp_common.connection.websocket import WebSocketClient

def main(sock:Union[TCPServer,TCPClient, SSHServer, WebSocketClient], inifile:configparser.ConfigParser, received:list, name:str, log_info:LogInfo):
    agent = player.agent.Agent(inifile=inifile,name=name,log_info=log_info)
    if received != None: agent.set_received(received=received)

    while agent.gameContinue:

        if len(agent.received) == 0:
            agent.parse_info(receive=sock.receive())
        
        agent.get_info()
        message = agent.action()

        if Action.is_initialize(request=agent.protocol.request):
            agent = lib.util.init_role(agent=agent,inifile=inifile, name=name, log_info=log_info)

        if message != "":
            sock.send(message=message)

    return agent.received if len(agent.received) != 0 else None

if __name__ == "__main__":
    config_path = "./res/config.ini"

    inifile = util.read_config_file(config_file_path=config_path)

    while True:

        sock = util.get_socket(inifile=inifile)
        sock.connect()

        received = None
        
        for _ in range(inifile.getint("game","num")):
            received = main(sock=sock, inifile=inifile, received=received, name=inifile.get("agent","name1"))
        
        sock.close()

        if not inifile.getboolean("connection","keep_connection"):
            break
