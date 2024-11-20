import configparser
import errno
import glob
import os
import random
import re
import shutil
import time
from pathlib import Path

from aiwolf_nlp_common.role import RoleInfo

import player
from lib.log import LogInfo


def read_text(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def random_select(data: list):
    return random.choice(data)


def is_json_complate(responces: bytes) -> bool:
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


def is_include_text(result: str) -> bool:
    return "{" in result


def check_json_missing_part(responces: str) -> int:
    count = 0

    for word in responces:
        if word == "{":
            count += 1
        elif word == "}":
            count -= 1

    return count


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


def is_file_exists(file_path: str) -> bool:
    return os.path.isfile(file_path)


def is_directory_exists(directory_path: str) -> bool:
    return Path(directory_path).is_dir()


def make_directory(directory_path: str) -> None:
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def delete_file(delete_file_path: str) -> None:
    if not is_file_exists(file_path=delete_file_path):
        return

    os.remove(path=delete_file_path)


def get_directories(path: str) -> list:
    if not is_directory_exists(directory_path=path):
        return []

    return [f.name for f in os.scandir(path=path) if f.is_dir()]


def get_directory_files(directory_path: str) -> list:
    wild_card: str = os.sep + "*"

    if not directory_path.endswith(wild_card):
        directory_path += wild_card

    return glob.glob(directory_path)


def move_log(current_path: str, next_path: str) -> None:
    if not is_directory_exists(directory_path=current_path):
        return

    if not is_directory_exists(directory_path=next_path):
        shutil.move(current_path, next_path)
    else:
        raise ValueError(next_path + "is alreadly exists")


def get_index_from_name(agent_name: str) -> int:
    return int(re.search(r"\d+", agent_name).group())


def index_to_agent_format(agent_index: int) -> str:
    return "Agent[{agent_index:0>2d}]".format(agent_index=agent_index)


def wait(wait_time: int) -> None:
    start_time = time.time()

    while time.time() - start_time < wait_time:
        pass
        pass
