import configparser
import inspect
import json
from timeout_decorator import timeout
from typing import Callable
from lib import util
from lib.AIWolf.commands import AIWolfCommand

class Agent:
    def __init__(self, inifile:configparser.ConfigParser, name:str) -> None:
       self.time_limit = 1
       self.name = name
       self.received = []
       self.gameContinue = True

       randomTalk = inifile.get("randomTalk","path")
       _ = util.check_config(randomTalk)
       
       self.comments = util.read_text(randomTalk)

    def with_timelimit(func:Callable):

        def _wrapper(self, *args, **keywords):
            time_limit = 0

            # set time limit
            if self.time_limit == 0 and keywords.get("time_limit") is None:
                raise ValueError(func.__name__ + ": time limit is not found")
            elif self.time_limit == 0:
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
            
            # call local function
            result = execute_func(self, *args, **keywords)

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
        self.index = self.gameInfo["agent"]
        self.role = self.gameInfo["roleMap"][str(self.index)]

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
    
    def hand_over(self, prev_agent:"Agent") -> None:

        func_name = set()
        local_values = set()

        for method in inspect.getmembers(prev_agent,inspect.ismethod):
            method_name = method[0]
            method_value = method[1]
            func_name.add(method_name)

            for func in inspect.getmembers(method_value,inspect.isfunction):
                func_value = func[1]

                for code in inspect.getmembers(func_value,inspect.iscode):
                    code_value = code[1]
                    # get all local func and variables name
                    local_values.update(set(code_value.co_names))

        # func and variables - func = variables
        local_values.difference_update(func_name)
        
        # hand over local variables
        for value_name in local_values:
            if hasattr(prev_agent,value_name):
                setattr(self,value_name,getattr(prev_agent,value_name))