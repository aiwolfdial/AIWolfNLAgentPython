import json
import lib

class Agent:
    def __init__(self, config_path:str, name:str) -> None:
       self.name = name
       self.received = []
       self.gameContinue = True

       inifile = lib.util.check_config(config_path=config_path)
       inifile.read(config_path,"UTF-8")

       randomTalk = inifile.get("randomTalk","path")
       _ = lib.util.check_config(randomTalk)
       
       self.comments = lib.util.read_text(randomTalk)

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
        return lib.util.random_select(self.comments)

    def vote(self) -> str:
        data = {"agentIdx":lib.util.random_select(self.alive)}

        return json.dumps(data,separators=(",",":"))

    def whisper(self) -> None:
        pass

    def finish(self) -> str:
        pass

    def action(self) -> str:

        if self.request == "INITIALIZE":
            self.initialize()
        elif self.request == "NAME":
            return self.get_name()
        elif self.request == "ROLE":
            return self.get_role()
        elif self.request == "DAILY_INITIALIZE":
            self.daily_initialize()
        elif self.request == "DAILY_FINISH":
            self.daily_finish()
        elif self.request == "TALK":
            return self.talk()
        elif self.request == "VOTE":
            return self.vote()
        elif self.request == "WHISPER":
            self.whisper()
        elif self.request == "FINISH":
            self.gameContinue = False
        
        return ""
    
    def hand_over(self, new_agent) -> None:
        # __init__
        new_agent.name = self.name
        new_agent.received = self.received
        new_agent.gameContinue = self.gameContinue
        new_agent.comments = self.comments

        # get_info
        new_agent.gameInfo = self.gameInfo
        new_agent.gameSetting = self.gameSetting
        new_agent.request = self.request
        new_agent.talkHistory = self.talkHistory
        new_agent.whisperHistory = self.whisperHistory

        # initialize
        new_agent.index = self.index
        new_agent.role = self.role