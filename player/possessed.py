import player
import lib

import json

class Possessed(player.agent.Agent):
    def __init__(self, config_path: str, name: str) -> None:
        super().__init__(config_path, name)

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