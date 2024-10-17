import configparser
import inspect
import math
from timeout_decorator import timeout, TimeoutError
from typing import Callable
from lib.log import LogInfo, AgentLog
from aiwolf_nlp_common import Action
from aiwolf_nlp_common import util
from aiwolf_nlp_common.connection import Connection
from aiwolf_nlp_common.protocol import CommunicationProtocol

class Agent:
    def __init__(self, inifile:configparser.ConfigParser, name:str, log_info:LogInfo, is_hand_over:bool=False):
        self.time_limit:float = 1.0
        self.name:str = name
        self.received:list = []
        self.gameContinue:bool = True
        
        if not is_hand_over:
            self.logger = AgentLog(inifile=inifile, agent_name=name, log_info=log_info)
        
        self.comments:list = util.read_text_file(text_file_path=inifile.get("filePath","random_talk"))

    def with_timelimit(func:Callable):

        def _wrapper(self, *args, **keywords):
            time_limit:float = 0.0
            result:str = ""

            # set time limit
            if math.isclose(self.time_limit, 0, abs_tol=1e-10)  and keywords.get("time_limit") is None:
                raise ValueError(func.__name__ + ": time limit is not found")
            elif math.isclose(self.time_limit, 0, abs_tol=1e-10):
                time_limit = keywords.get("time_limit")
            elif keywords.get("time_limit") is None:
                time_limit = self.time_limit
            else:
                time_limit = min(self.time_limit, keywords.get("time_limit"))

            # define local function
            @timeout(time_limit)
            def execute_func(self, *args, **keywords):
                # execute function
                if len(keywords) == 0:
                    result = func(self)
                else:
                    result = func(self, *args, **keywords)

                return result
            
            try:
                # call local function
                result = execute_func(self, *args, **keywords)
            except TimeoutError:
                print(func.__name__ + " has run out of time.")

            return result

        return _wrapper
    
    def send_agent_index(func:Callable):
        
        def _wrapper(self,*args, **keywords):
            
            # execute function
            if len(keywords) == 0:
                result:int = func(self)
            else:
                result:int = func(self, *args, **keywords)

            if type(result) is not int:
                raise ValueError("Functions with the send_agent_index decorator must return an int type")
            
            return util.index_to_agent_format(agent_index=result)
        
        return _wrapper

    def set_received(self, received:list) -> None:
        self.received = received

    def parse_info(self, receive: str) -> None:
        self.received = receive
    
    def get_info(self):
        self.protocol = CommunicationProtocol.initialize_from_json(received_str=self.received.pop(0))
   
    def initialize(self) -> None:
        self.agent_name:str = self.protocol.game_info.agent
        self.index:int = util.get_index_from_name(agent_name=self.agent_name)

        self.time_limit:float = self.protocol.game_setting.get_action_timeout_in_seconds()
        self.role:str = self.protocol.game_info.role_map.get_agent_role(agent=self.agent_name)

    def daily_initialize(self) -> None:
        self.alive = self.protocol.game_info.status_map.get_alive_agent_list()

    def daily_finish(self) -> None:
        pass
    
    @with_timelimit
    def get_name(self) -> str:
        return self.name
    
    @with_timelimit
    def get_role(self) -> str:
        return self.role
    
    @with_timelimit
    def talk(self) -> str:
        comment:str = util.random_select(self.comments)
        self.logger.talk(comment=comment)
        return comment
    
    @with_timelimit
    @send_agent_index
    def vote(self) -> int:
        vote_target:int = util.random_select(self.alive)
        self.logger.vote(vote_target=vote_target)
        return vote_target
    
    @with_timelimit
    def whisper(self) -> None:
        pass

    def finish(self) -> str:
        self.gameContinue = False
        self.logger.close()

    def action(self) -> str:

        if Action.is_initialize(request=self.protocol.request):
            self.initialize()
        elif Action.is_name(request=self.protocol.request):
            return self.get_name()
        elif Action.is_role(request=self.protocol.request):
            return self.get_role()
        elif Action.is_daily_initialize(request=self.protocol.request):
            self.daily_initialize()
        elif Action.is_daily_finish(request=self.protocol.request):
            self.daily_finish()
        elif Action.is_talk(request=self.protocol.request):
            return self.talk()
        elif Action.is_vote(request=self.protocol.request):
            return self.vote()
        elif Action.is_whisper(request=self.protocol.request):
            self.whisper()
        elif Action.is_finish(request=self.protocol.request):
            self.finish()
        
        return ""
    
    def hand_over(self, new_agent) -> None:
        # __init__
        new_agent.name = self.name
        new_agent.received = self.received
        new_agent.gameContinue = self.gameContinue
        new_agent.comments = self.comments
        new_agent.received = self.received
        new_agent.logger = self.logger

        # get_info
        if hasattr(self,'gameInfo'):
            new_agent.gameInfo = self.gameInfo
        
        if hasattr(self,'gameSetting'):
            new_agent.gameSetting = self.gameSetting

        if hasattr(self,'talkHistory'):
            new_agent.talkHistory = self.talkHistory
        
        if hasattr(self,'whisperHistory'):
            new_agent.whisperHistory = self.whisperHistory

        new_agent.request = self.protocol.request

        # initialize
        new_agent.index = self.index
        new_agent.role = self.role
        new_agent.time_limit = self.time_limit