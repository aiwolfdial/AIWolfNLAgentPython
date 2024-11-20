import configparser
from typing import Union

from aiwolf_nlp_common import Action, util
from aiwolf_nlp_common.connection.ssh import SSHServer
from aiwolf_nlp_common.connection.tcp import TCPClient, TCPServer
from aiwolf_nlp_common.connection.websocket import WebSocketClient

import lib
import player
from lib.log import LogInfo


def main(
    sock: Union[TCPServer, TCPClient, SSHServer, WebSocketClient],
    inifile: configparser.ConfigParser,
    received: list,
    name: str,
    log_info: LogInfo,
):
    agent = player.agent.Agent(inifile=inifile, name=name, log_info=log_info)
    if received != None:
        agent.set_received(received=received)

    while agent.gameContinue:
        if len(agent.received) == 0:
            agent.parse_info(receive=sock.receive())

        agent.get_info()
        message = agent.action()

        if Action.is_initialize(request=agent.protocol.request):
            agent = lib.util.init_role(
                agent=agent, inifile=inifile, name=name, log_info=log_info
            )

        if message != "":
            sock.send(message=message)

    return agent.received if len(agent.received) != 0 else None


if __name__ == "__main__":
    config_path = "./res/config.ini"

    inifile = util.read_config_file(config_file_path=config_path)

    log_info = LogInfo()

    while True:
        sock = util.get_socket(inifile=inifile, name=inifile.get("agent", "name1"))
        sock.connect()

        received = None

        for _ in range(inifile.getint("game", "num")):
            received = main(
                sock=sock,
                inifile=inifile,
                received=received,
                name=inifile.get("agent", "name1"),
                log_info=log_info,
            )

        sock.close()

        if not inifile.getboolean("connection", "keep_connection"):
            break
