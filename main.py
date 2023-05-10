import lib
import player

def main(config_path:str, name:str):
    client = lib.client.Client(config_path=config_path)
    client.connet()

    agent = player.agent.Agent(config_path=config_path,name=name)

    while agent.gameContinue:

        if len(agent.received) == 0:
            agent.parse_info(receive=client.receive())
        
        agent.get_info()
        message = agent.action()

        if agent.request == "INITIALIZE":
            agent = lib.util.init_role(agent=agent, config_path=config_path, name=name)

        if message != "":
            client.send(message=message)

    client.close()

if __name__ == "__main__":
    config_path = "./res/config.ini"

    inifile = lib.util.check_config(config_path=config_path)
    inifile.read(config_path,"UTF-8")

    main(config_path=config_path, name=inifile.get("agent","name1"))