import configparser
from lib import util
from lib.log import LogInfo
from player.agent import Agent
from aiwolf_nlp_common import Action

class Werewolf(Agent):
    
    def __init__(self, inifile: configparser.ConfigParser, name: str, log_info: LogInfo, is_hand_over: bool = False):
        super().__init__(inifile, name, log_info, is_hand_over)
    
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
    
    @Agent.with_timelimit
    def get_name(self) -> str:
        return super().get_name()
    
    @Agent.with_timelimit
    def get_role(self) -> str:
        return super().get_role()
    
    @Agent.with_timelimit
    def talk(self) -> str:
        return super().talk()
    
    @Agent.with_timelimit
    def vote(self) -> int:
        return super().vote()
    
    @Agent.with_timelimit
    def whisper(self) -> None:
        return super().whisper()
    
    @Agent.with_timelimit
    @Agent.send_agent_index
    def attack(self) -> int:
        attack_target:int = util.random_select(self.alive)
        self.logger.attack(attack_target=attack_target)
        return attack_target
    
    def action(self) -> str:

        if Action.is_attack(request=self.protocol.request):
            return self.attack()
        else:
            return super().action()
    
    def hand_over(self, new_agent) -> None:
        return super().hand_over(new_agent)