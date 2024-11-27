import configparser
import re
from pathlib import Path

from aiwolf_nlp_common.role import RoleInfo

import player
from lib.log_info import LogInfo


def init_role(
    agent: player.agent.Agent,
    inifile: configparser.ConfigParser,
    name: str,
    log_info: LogInfo,
) -> player.agent.Agent:
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
    else:
        raise ValueError(agent.role, "Role is not defined")
    agent.hand_over(new_agent=new_agent)
    return new_agent


def get_dirs(path: Path) -> list:
    if not path.exists():
        return []
    return [d.name for d in path.iterdir() if d.is_dir()]


def agent_name_to_idx(name: str) -> int:
    match = re.search(r"\d+", name)
    if match is None:
        raise ValueError(name, "No number found in agent name")
    return int(match.group())


def agent_idx_to_agent(idx: int) -> str:
    return f"Agent[{idx:0>2d}]"
