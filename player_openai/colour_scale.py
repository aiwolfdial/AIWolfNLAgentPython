from player_openai.info_types import TalkHistory, GameInfo
from player_openai.functions.get_colour_scale import get_colour_scale


class Colour_Scale():
    """
    他プレイヤーのグレー度合い
    """
    def __init__(self, my_agent_id: str, my_agent_role: str, target_agent_id: str) -> None:
        # 基本情報
        self.target_agent_id: str = target_agent_id
        self.my_agent_id: str = my_agent_id
        self.my_agent_role: str = my_agent_role
        self.alive: bool = True
        # 考察
        self.day_colour_scales: dict[int, str] = {} # 日毎のグレー度合い
        # self.habit = None

    def update_alive(self, alive: bool) -> None:
        self.alive = alive
    
    def update(self, day: int, talk_history: TalkHistory) -> None:
        if not self.alive:
            return

        # 最初の発言の場合はupdate不要
        if len(talk_history) == 0:
            return

        colour_scale: str = get_colour_scale(self.my_agent_id, self.my_agent_role, self.target_agent_id, self.day_colour_scale, talk_history)

        # 同じ日のスタンスを上書き
        self.day_colour_scales[day-1] = colour_scale