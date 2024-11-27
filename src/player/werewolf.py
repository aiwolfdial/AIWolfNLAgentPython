from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import configparser

    from lib.log_info import LogInfo

import random

from aiwolf_nlp_common import Action

from lib import util
from player.agent import Agent


class Werewolf(Agent):
    def __init__(
        self,
        inifile: configparser.ConfigParser,
        name: str,
        log_info: LogInfo,
        is_hand_over: bool = False,
    ) -> None:
        super().__init__(inifile, name, log_info, is_hand_over)

    def parse_info(self, receive: str | list[str]) -> None:
        return super().parse_info(receive)

    def get_info(self) -> None:
        return super().get_info()

    def initialize(self) -> None:
        return super().initialize()

    def daily_initialize(self) -> None:
        return super().daily_initialize()

    def daily_finish(self) -> None:
        return super().daily_finish()

    @Agent.timeout
    def get_name(self) -> str:
        return super().get_name()

    @Agent.timeout
    def get_role(self) -> str:
        return super().get_role()

    @Agent.timeout
    def talk(self) -> str:
        return super().talk()

    @Agent.timeout
    def vote(self) -> int:
        return super().vote()

    @Agent.timeout
    def whisper(self) -> None:
        return super().whisper()

    @Agent.timeout
    @Agent.send_agent_index
    def attack(self) -> int:
        attack_target: int = util.agent_name_to_idx(random.choice(self.alive))
        self.logger.attack(attack_target=attack_target)
        return attack_target

    def action(self) -> str:
        if Action.is_attack(request=self.protocol.request):
            return self.attack()
        return super().action()

    def hand_over(self, new_agent: Agent) -> None:
        return super().hand_over(new_agent)
