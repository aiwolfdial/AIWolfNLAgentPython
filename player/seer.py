import configparser
from lib import util
from lib.log import LogInfo
from player.agent import Agent

class Seer(Agent):
    
    def __init__(self, inifile: configparser.ConfigParser, name: str, log_info: LogInfo, is_hand_over: bool = False):
        super().__init__(inifile, name, log_info, is_hand_over)
    
    @Agent.with_timelimit
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
    
    def get_name(self) -> str:
        # print("Get Name")
        return super().get_name()
    
    def get_role(self) -> str:
        return super().get_role()
    
    @Agent.with_timelimit
    def talk(self) -> str:
        # util.wait(wait_time=10)
        return super().talk()
    
    def vote(self) -> int:
        return super().vote()
    
    def whisper(self) -> None:
        return super().whisper()
    
    @Agent.send_agent_index
    def divine(self) -> int:
        return util.random_select(self.alive)
    
    def action(self) -> str:

        if self.request == "DIVINE":
            return self.divine()
        else:
            return super().action()
    
    def hand_over(self, new_agent) -> None:
        return super().hand_over(new_agent)