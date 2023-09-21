import configparser
import json
from lib import(
    util
)
from res.Commands import Command

class Agent:
    def __init__(self, inifile:configparser.ConfigParser, name:str) -> None:
       self.name = name
       self.received = []
       self.gameContinue = True

       randomTalk = inifile.get("randomTalk","path")
       _ = util.check_config(randomTalk)
       
       self.comments = util.read_text(randomTalk)
    
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
    
    def get_name(self) -> str:
        return self.name
    
    def get_role(self) -> str:
        return self.role
    
    def talk(self) -> str:
        return util.random_select(self.comments)

    def vote(self) -> str:
        data = {"agentIdx":util.random_select(self.alive)}

        return json.dumps(data,separators=(",",":"))

    def whisper(self) -> None:
        pass

    def finish(self) -> str:
        self.gameContinue = False

    def action(self) -> str:

        if Command.is_initialize(request=self.request):
            self.initialize()
        elif Command.is_name(request=self.request):
            return self.get_name()
        elif Command.is_role(request=self.request):
            return self.get_role()
        elif Command.is_daily_initialize(request=self.request):
            self.daily_initialize()
        elif Command.is_daily_finish(request=self.request):
            self.daily_finish()
        elif Command.is_talk(request=self.request):
            return self.talk()
        elif Command.is_vote(request=self.request):
            return self.vote()
        elif Command.is_whisper(request=self.request):
            self.whisper()
        elif Command.finish(request=self.request):
            self.finish()
        
        return ""
    
    def hand_over(self, new_agent) -> None:
        # __init__
        new_agent.name = self.name
        new_agent.received = self.received
        new_agent.gameContinue = self.gameContinue
        new_agent.comments = self.comments
        new_agent.received = self.received

        # get_info
        new_agent.gameInfo = self.gameInfo
        new_agent.gameSetting = self.gameSetting
        new_agent.request = self.request
        new_agent.talkHistory = self.talkHistory
        new_agent.whisperHistory = self.whisperHistory

        # initialize
        new_agent.index = self.index
        new_agent.role = self.role