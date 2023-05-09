import os
import errno
import configparser
import random
import player

def read_text(path:str):
    with open(path,"r",encoding="utf-8") as f:
        return f.read().splitlines()

def random_select(data:list):
    return random.choice(data)

def is_json_complate(responces:bytes) -> bool:

    try:
        responces = responces.decode("utf-8")
    except:
        return False
    
    if responces == "":
        return False

    cnt = 0

    for word in responces:
        if word == "{":
            cnt += 1
        elif word == "}":
            cnt -= 1
    
    return cnt == 0

def init_role(agent:player.agent.Agent, config_path:str, name:str):
    if agent.role == "VILLAGER":
        new_agent = player.villager.Villager(config_path=config_path, name=name)
    elif agent.role == "WEREWOLF":
        new_agent = player.werewolf.Werewolf(config_path=config_path, name=name)
    elif agent.role == "SEER":
        new_agent = player.seer.Seer(config_path=config_path, name=name)
    elif agent.role == "POSSESSED":
        new_agent = player.possessed.Possessed(config_path=config_path, name=name)

    agent.hand_over(new_agent=new_agent)

    return new_agent

def check_config(config_path:str) -> configparser.ConfigParser:

    if not os.path.exists(config_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_path)
    
    return configparser.ConfigParser()