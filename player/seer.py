import configparser
import json
import player
import lib
from lib import util
from player.agent import Agent

class Seer(player.agent.Agent):
    def __init__(self, inifile:configparser.ConfigParser, name:str) -> None:
        super().__init__(inifile=inifile, name=name)
    
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
        print("Get Name")
        return super().get_name()
    
    def get_role(self) -> str:
        return super().get_role()
    
    @Agent.with_timelimit
    def talk(self) -> str:
        util.wait(wait_time=10)
        return super().talk()
    
    def vote(self) -> str:
        return super().vote()
    
    def whisper(self) -> None:
        return super().whisper()

    def divine(self) -> str:
        data = {"agentIdx":lib.util.random_select(self.alive)}

        return json.dumps(data,separators=(",",":"))
    
    def action(self) -> str:

        if self.request == "DIVINE":
            return self.divine()
        else:
            return super().action()
    
    def hand_over(self, new_agent) -> None:
        return super().hand_over(new_agent)