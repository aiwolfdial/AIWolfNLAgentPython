from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum


class Agent:
    idx: int
    name: str


class Species(str, Enum):
    HUMAN = "HUMAN"
    WEREWOLF = "WEREWOLF"
    ANY = "ANY"


class Talk:
    model_config = {"arbitrary_types_allowed": True}

    idx: int
    day: int
    turn: int
    agent: "Agent"  # 前方参照
    text: str
    OVER = "Over"
    SKIP = "Skip"
    FORCE_SKIP = "ForceSkip"


# TalkHistoryをList[Talk]として定義
class TalkHistory(List[Talk]):
    """
    その日のそれまでの会話のリスト。
    """


class Role(str, Enum):
    BODYGUARD = "BODYGUARD"
    FREEMASON = "FREEMASON"
    MEDIUM = "MEDIUM"
    POSSESSED = "POSSESSED"
    SEER = "SEER"
    VILLAGER = "VILLAGER"
    WEREWOLF = "WEREWOLF"
    FOX = "FOX"
    ANY = "ANY"


class Judge:
    model_config = {"arbitrary_types_allowed": True}

    day: int
    agent: Agent
    target: Agent
    result: Species


class Role(str, Enum):
    BODYGUARD = "BODYGUARD"
    FREEMASON = "FREEMASON"
    MEDIUM = "MEDIUM"
    POSSESSED = "POSSESSED"
    SEER = "SEER"
    VILLAGER = "VILLAGER"
    WEREWOLF = "WEREWOLF"
    FOX = "FOX"
    ANY = "ANY"


class Vote:
    model_config = {"arbitrary_types_allowed": True}

    day: int
    agent: Agent
    target: Agent


class Status(str, Enum):
    ALIVE = "ALIVE"
    DEAD = "DEAD"


class GameInfo(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    day: int
    agent: Optional[Agent]
    mediumResult: Optional[Judge] = None
    divineResult: Optional[Judge] = None
    executedAgent: Optional[Agent] = None
    latestExecutedAgent: Optional[Agent] = None
    attackedAgent: Optional[Agent] = None
    cursedFox: Optional[Agent] = None
    guardedAgent: Optional[Agent] = None
    voteList: List[Vote] = []
    latestVoteList: List[Vote] = []
    attackVoteList: List[Vote] = []
    latestAttackVoteList: List[Vote] = []
    talkList: List[Talk] = []
    whisperList: List[Talk] = []
    statusMap: Dict[Agent, Status] = {}
    roleMap: Dict[Agent, Role] = {}
    remainTalkMap: Dict[Agent, int] = {}
    remainWhisperMap: Dict[Agent, int] = {}
    existingRoleList: List[Role] = []
    lastDeadAgentList: List[Agent] = []

