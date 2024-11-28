from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import configparser

    from utils.log_info import LogInfo

import random

from aiwolf_nlp_common import Action

from player.agent import Agent
from utils import agent_util


class Seer(Agent):
    def __init__(
        self,
        config: configparser.ConfigParser,
        name: str,
        log_info: LogInfo,
        is_hand_over: bool = False,
    ) -> None:
        super().__init__(config, name, log_info, is_hand_over)

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
        if self.protocol.info is None:
            return super().talk()
        if not self.protocol.info.divine_result.is_empty():
            self.logger.divine_result(
                divine_result=self.protocol.info.divine_result.result,
            )
            return self.protocol.info.divine_result.result

        return super().talk()

    @Agent.timeout
    def vote(self) -> int:
        return super().vote()

    @Agent.timeout
    def whisper(self) -> None:
        return super().whisper()

    @Agent.timeout
    @Agent.send_agent_index
    def divine(self) -> int:
        divine_target: int = agent_util.agent_name_to_idx(
            name=random.choice(self.alive),  # noqa: S311
        )
        self.logger.divine(divine_target=divine_target)
        return divine_target

    def action(self) -> str:
        if Action.is_divine(request=self.protocol.request):
            return self.divine()
        return super().action()

    def hand_over(self, new_agent: Agent) -> None:
        return super().hand_over(new_agent)
