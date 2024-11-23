import configparser
from lib import util
from lib.log import LogInfo
from player_openai.agent import Agent_OpenAI


class Seer(Agent_OpenAI):

    def __init__(
        self,
        inifile: configparser.ConfigParser,
        name: str,
        log_info: LogInfo,
        is_hand_over: bool = False,
    ):
        super().__init__(inifile, name, log_info, is_hand_over)

    @Agent_OpenAI.with_timelimit
    def parse_info(self, receive: str) -> None:
        return super().parse_info(receive)

    def get_info(self):
        return super().get_info()

    def initialize(self) -> None:
        return super().initialize()

    def daily_initialize(self) -> None:
        return super().daily_initialize()

    def daily_finish(self) -> None:
        return super().daily_finish()

    @Agent_OpenAI.with_timelimit
    def get_name(self) -> str:
        return super().get_name()

    @Agent_OpenAI.with_timelimit
    def get_role(self) -> str:
        return super().get_role()

    @Agent_OpenAI.with_timelimit
    def talk(self) -> str:

        if self.gameInfo is not None and self.gameInfo.get("divineResult") is not None:
            divine_result: str = self.gameInfo["divineResult"]
            self.logger.divine_result(divine_result=divine_result)
            return divine_result.get("result")

        return super().talk()

    @Agent_OpenAI.with_timelimit
    def vote(self) -> int:
        return super().vote()

    @Agent_OpenAI.with_timelimit
    def whisper(self) -> None:
        return super().whisper()

    @Agent_OpenAI.with_timelimit
    @Agent_OpenAI.send_agent_index
    def divine(self) -> int:
        divine_target: int = util.random_select(self.alive)
        self.logger.divine(divine_target=divine_target)
        return divine_target

    def action(self) -> str:

        if self.request == "DIVINE":
            return self.divine()
        else:
            return super().action()

    def hand_over(self, new_agent) -> None:
        return super().hand_over(new_agent)
