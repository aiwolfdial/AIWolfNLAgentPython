from player_openai.stance import Stance
from player_openai.colour_scale import Colour_Scale
from player_openai.coming_out import Coming_Out
from player_openai.functions.get_tactic import get_tactic

# from player_openai.functions.get_vote_target import get_vote_target
import random
from typing import Dict

# from player_openai.dev_functions.log import log


class MyTactics:
    def __init__(
        self, day: int, my_agent_id: str, my_agent_role: str, roleNumMap: Dict[str, int]
    ) -> None:
        self.day: int = day
        self.my_agent_id: str = my_agent_id
        self.my_agent_role: str = my_agent_role
        self.roleNumMap: Dict[str, int] = roleNumMap
        self.tactics: dict[int, str] = {}

    def update(
        self,
        day: int,
        stances: list[Stance],
        colour_scales: list[Colour_Scale],
        coming_outs: list[Coming_Out],
    ):
        tactic: str = get_tactic(
            self.day,
            self.my_agent_id,
            self.my_agent_role,
            self.roleNumMap,
            stances,
            colour_scales,
            coming_outs,
            self.tactics,
        )

        self.tactics[day - 1] = tactic  # 同じ日のスタンスは上書き

    # def decide_vote_target(self, agent_id: int, agent_role: str, alive: list[int]):
    #     for _ in range(5):
    #         target_id : int = get_vote_target(agent_id, agent_role, alive, self.tactics)

    #         # target_idが生きているか
    #         if target_id not in alive: continue

    #         # target_idが自分自身でないか
    #         if target_id == agent_id: continue

    #         # print(f"投票先を決定: 自分のid: {agent_id}, target: {target_id}")
    #         log(agent_id,[f"投票先を決定: 自分のid: {agent_id}, target: {target_id}"])
    #         return target_id
    #     # print("Error: 5回試行しても投票先が決まらなかった")
    #     target = random.choice(alive)
    #     # print(f"ランダムに投票先を決定: 自分のid: {agent_id}, target: {target}")
    #     log(agent_id, ["Error: 5回試行しても投票先が決まらなかった", f"ランダムに投票先を決定: 自分のid: {agent_id}, target: {target}"])
    #     return target
