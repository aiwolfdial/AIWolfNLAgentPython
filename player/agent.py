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
    
    def set_received(self, received:list) -> None:
        self.received = received

    def parse_info(self, receive: str) -> None:

        received_list = receive.split("}\n{")

        for index in range(len(received_list)):
            received_list[index] = received_list[index].rstrip()

            if received_list[index][0] != "{":
                received_list[index] = "{" + received_list[index]

            if received_list[index][-1] != "}":
                received_list[index] += "}"

            self.received.append(received_list[index])
    
    def get_info(self):
        data = json.loads(self.received.pop(0))

        self.gameInfo = data["gameInfo"]
        self.gameSetting = data["gameSetting"]
        self.request = data["request"]
        self.talkHistory = data["talkHistory"]
        self.whisperHistory = data["whisperHistory"]
   
    def initialize(self) -> None:
        self.index:int = self.gameInfo["agent"]
        self.time_limit:float = int(self.gameSetting["actionTimeout"])/1000 # ms指定でくるのでsに変換
        self.role:str = self.gameInfo["roleMap"][str(self.index)]

    def daily_initialize(self) -> None:
        self.alive = []

        for agent_num in self.gameInfo["statusMap"]:

            if self.gameInfo["statusMap"][agent_num] == "ALIVE" and int(agent_num) != self.index:
                self.alive.append(int(agent_num))

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
        return util.random_select(self.comments)
    
    @with_timelimit
    def vote(self) -> str:
        data = {"agentIdx":util.random_select(self.alive)}

        return json.dumps(data,separators=(",",":"))
    
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
        new_agent.gameInfo = self.gameInfo
        new_agent.gameSetting = self.gameSetting
        new_agent.request = self.request
        new_agent.talkHistory = self.talkHistory
        new_agent.whisperHistory = self.whisperHistory

        # initialize
        new_agent.index = self.index
        new_agent.role = self.role
        new_agent.time_limit = self.time_limit