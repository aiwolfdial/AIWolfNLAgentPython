import configparser
import player
from player.agent import Agent

class Villager(player.agent.Agent):
    def __init__(self, inifile:configparser.ConfigParser, name:str) -> None:
        super().__init__(inifile=inifile, name=name)
    
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
        return super().get_name()
    
    def get_role(self) -> str:
        return super().get_role()
    
    def talk(self) -> str:
        
        return super().talk()
    
    def vote(self) -> str:
        return super().vote()
    
    def whisper(self) -> None:
        return super().whisper()

    def action(self) -> str:
        return super().action()
    
    def hand_over(self, new_agent) -> None:
        return super().hand_over(new_agent)