import configparser
import lib
import player
from res.Commands import Command

def main(client:lib.client.Client, inifile:configparser.ConfigParser, received:list, name:str):
    agent = player.agent.Agent(inifile=inifile,name=name)
    if received != None: agent.set_received(received=received)

    while agent.gameContinue:

        if len(agent.received) == 0:
            agent.parse_info(receive=client.receive())
        
        agent.get_info()
        message = agent.action()

        if Command.is_initialize(request=agent.request):
            agent = lib.util.init_role(agent=agent, config_path=config_path, name=name)

        if message != "":
            client.send(message=message)

    return agent.received if len(agent.received) != 0 else None

if __name__ == "__main__":
    config_path = "./res/config.ini"

    inifile = lib.util.check_config(config_path=config_path)
    inifile.read(config_path,"UTF-8")

     # connect to server
    client = lib.client.Client(config_path=config_path)
    client.connect()

    received = None
    
    for _ in range(inifile.getint("game","num")):
        received = main(client=client, inifile=inifile, received=received, name=inifile.get("agent","name1"))

    client.close()