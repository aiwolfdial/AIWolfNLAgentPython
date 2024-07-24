import configparser
import inspect
import math
import json
from timeout_decorator import timeout, TimeoutError
from typing import Callable
from lib import util
from lib.AIWolf.commands import AIWolfCommand
from lib.log import LogInfo, AgentLog

class Agent:
    def __init__(self, inifile:configparser.ConfigParser, name:str, log_info:LogInfo, is_hand_over:bool=False):
       self.time_limit:float = 1.0
       self.name:str = name
       self.received:list = []
       self.gameContinue:bool = True

       if not is_hand_over:
           self.logger = AgentLog(inifile=inifile, agent_name=name, log_info=log_info)

       random_talk_path:str = inifile.get("filePath","random_talk")
       _ = util.check_config(random_talk_path)
       
       self.comments:list = util.read_text(random_talk_path)

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

        received_list = receive.split("}\n{")

        for index in range(len(received_list)):
            received_list[index] = received_list[index].rstrip()

            count = util.check_json_missing_part(responces=received_list[index])

            while count < 0:
                received_list[index] = "{" + received_list[index]
                count += 1
            
            while count > 0:
                received_list[index] += "}"
                count -= 1

            self.received.append(received_list[index])
    
    def get_info(self):
        try:
            test = self.received.pop(0)
            data = json.loads(test)
        except:
            print(test)
            data = json.loads(test)

        if data.get("gameInfo") is not None:
            self.gameInfo = data["gameInfo"]
        
        if data.get("gameSetting") is not None:
            self.gameSetting = data["gameSetting"]

        if data.get("talkHistory") is not None:
            self.talkHistory = data["talkHistory"]
        
        if data.get("whisperHistory") is not None:
            self.whisperHistory = data["whisperHistory"]

        self.request = data["request"]

        self.logger.get_info(get_info=data, request=self.request)
   
    def initialize(self) -> None:
        self.index:int = util.get_index_from_name(agent_name=self.gameInfo["agent"])

        self.time_limit:float = int(self.gameSetting["actionTimeout"])/1000 # ms -> s
        self.role:str = self.gameInfo["roleMap"][self.gameInfo["agent"]]

    def daily_initialize(self) -> None:
        self.alive = []

        for agent_name in self.gameInfo["statusMap"]:
            agent_num:int = util.get_index_from_name(agent_name=agent_name)

            if self.gameInfo["statusMap"][agent_name] == "ALIVE" and agent_num != self.index:
                self.alive.append(agent_num)

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

    def action(self) -> str:

        if AIWolfCommand.is_initialize(request=self.request):
            self.initialize()
        elif AIWolfCommand.is_name(request=self.request):
            return self.get_name()
        elif AIWolfCommand.is_role(request=self.request):
            return self.get_role()
        elif AIWolfCommand.is_daily_initialize(request=self.request):
            self.daily_initialize()
        elif AIWolfCommand.is_daily_finish(request=self.request):
            self.daily_finish()
        elif AIWolfCommand.is_talk(request=self.request):
            return self.talk()
        elif AIWolfCommand.is_vote(request=self.request):
            return self.vote()
        elif AIWolfCommand.is_whisper(request=self.request):
            self.whisper()
        elif AIWolfCommand.is_finish(request=self.request):
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

        new_agent.request = self.request

        # initialize
        new_agent.index = self.index
        new_agent.role = self.role
        new_agent.time_limit = self.time_limit