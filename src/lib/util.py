import configparser
import errno
import os
import random
import re
from pathlib import Path

from aiwolf_nlp_common.role import RoleInfo

import player
from lib.log import LogInfo


def random_select(data: list):
    return random.choice(data)


def init_role(
    agent: player.agent.Agent,
    inifile: configparser.ConfigParser,
    name: str,
    log_info: LogInfo,
):
    if RoleInfo.is_villager(role=agent.role):
        new_agent = player.villager.Villager(
            inifile=inifile, name=name, log_info=log_info, is_hand_over=True
        )
    elif RoleInfo.is_werewolf(role=agent.role):
        new_agent = player.werewolf.Werewolf(
            inifile=inifile, name=name, log_info=log_info, is_hand_over=True
        )
    elif RoleInfo.is_seer(role=agent.role):
        new_agent = player.seer.Seer(
            inifile=inifile, name=name, log_info=log_info, is_hand_over=True
        )
    elif RoleInfo.is_possessed(role=agent.role):
        new_agent = player.possessed.Possessed(
            inifile=inifile, name=name, log_info=log_info, is_hand_over=True
        )

    agent.hand_over(new_agent=new_agent)
    # new_agent.hand_over(prev_agent=agent)

    return new_agent


def check_config(config_path: str) -> configparser.ConfigParser:
    if not os.path.exists(config_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_path)

    return configparser.ConfigParser()


def is_directory_exists(directory_path: str) -> bool:
    return Path(directory_path).is_dir()


def make_directory(directory_path: str) -> None:
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def get_directories(path: str) -> list:
    if not is_directory_exists(directory_path=path):
        return []

    return [f.name for f in os.scandir(path=path) if f.is_dir()]


def get_index_from_name(agent_name: str) -> int:
    return int(re.search(r"\d+", agent_name).group())


def index_to_agent_format(agent_index: int) -> str:
    return "Agent[{agent_index:0>2d}]".format(agent_index=agent_index)
