import json
import configparser
from player.agent import Agent
from player_openai.stance import Stance
from player_openai.colour_scale import Colour_Scale
from player_openai.coming_out import Coming_Out
from player_openai.my_tactics import MyTactics
import concurrent.futures
from lib import util

from player_openai.functions.generate_statement import generate_statement

from player_openai.info_types import TalkHistory
from typing import Union

from player_openai.dev_functions.log import clear_log, log, log_talk
from lib.log import LogInfo


class Agent_OpenAI(Agent):
    def __init__(
        self,
        inifile: configparser.ConfigParser,
        name: str,
        log_info: LogInfo,
        is_hand_over: bool = False,
    ) -> None:
        # 親クラス(Agent)の__init__を正しいパラメータで呼び出す
        super().__init__(inifile, name, log_info, is_hand_over)

        # ゲーム状況
        self.day: int = 0

        # 考察Class
        self.my_tactics = None
        self.stances = []
        self.colour_scale = []
        self.coming_out = []
        self.talkHistory = TalkHistory([])

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

        if data.get("request") is not None:
            self.request = data["request"]

    def initialize(self):
        """
        initializeを受け取ったタイミングで実行されるmethod
        """
        super().initialize()
        # 考察Classの初期化
        self.init_stances()
        self.init_colour_scales()
        self.init_coming_outs()
        self.init_tactics()

        clear_log(self.index)  # ログの初期化

    # def daily_initialize(self) -> None:
    #     self.alive = []
    #     for agent_num, stance in enumerate(self.stances):
    #         if self.gameInfo["statusMap"][str(agent_num + 1)] == "ALIVE":
    #             self.alive.append(agent_num + 1)
    #             stance.update_alive(True)
    #         else:
    #             stance.update_alive(False)

    #     for agent_num, colour_scale in enumerate(self.colour_scales):
    #         if self.gameInfo["statusMap"][str(agent_num + 1)] == "ALIVE":
    #             colour_scale.update_alive(True)
    #         else:
    #             colour_scale.update_alive(False)

    #     for agent_num, coming_out in enumerate(self.coming_outs):
    #         if self.gameInfo["statusMap"][str(agent_num + 1)] == "ALIVE":
    #             coming_out.update_alive(True)
    #         else:
    #             coming_out.update_alive(False)
    #     day: int = int(self.gameInfo["day"])
    #     self.day = day

    def _get_agent_status(self, agent_num: int) -> bool:
        """
        エージェントの生存状態を取得
        Args:
            agent_num (int): エージェント番号（0から始まる）
        Returns:
            bool: 生存していればTrue、死亡していればFalse
        """
        agent_id = f"Agent[{agent_num + 1:02d}]"
        return self.gameInfo["statusMap"][agent_id] == "ALIVE"

    def daily_initialize(self) -> None:
        """
        1日の始めに実行される初期化処理
        各エージェントの生存状態を更新する
        """
        self.alive = []

        # スタンス情報の更新
        for agent_num, stance in enumerate(self.stances):
            is_alive = self._get_agent_status(agent_num)
            if is_alive:
                self.alive.append(agent_num + 1)
            stance.update_alive(is_alive)

        # カラースケール情報の更新
        for agent_num, colour_scale in enumerate(self.colour_scales):
            colour_scale.update_alive(self._get_agent_status(agent_num))

        # カミングアウト情報の更新
        for agent_num, coming_out in enumerate(self.coming_outs):
            coming_out.update_alive(self._get_agent_status(agent_num))

        # 日付の更新
        self.day = int(self.gameInfo["day"])

    def talk(self) -> str:
        if self.day == 0:
            return "Over"

        # 他人のスタンスの更新
        self.update_stances()
        # 他人のカミングアウト状況の更新
        self.update_colour_scales()
        # 他人のカミングアウト状況の更新
        self.update_coming_outs()
        # 自分の戦略の更新
        self.update_my_tactics()
        # 発言（改行は含めない）
        statement = self.generate_statement().replace("\n", " ")
        self.save_talk_log(statement)
        return statement

    def save_talk_log(self, statement: str):
        # 各部分を個別に作成して結合
        stances_text = "\n".join(
            [
                f"{stance.target_agent_id} - {stance.day_stances}"
                for stance in self.stances
            ]
        )
        colour_scales_text = "\n".join(
            [
                f"{colour_scale.target_agent_id} - {colour_scale.day_colour_scales}"
                for colour_scale in self.colour_scales
            ]
        )
        coming_outs_text = "\n".join(
            [
                f"{coming_out.target_agent_id} - {coming_out.day_coming_outs}"
                for coming_out in self.coming_outs
            ]
        )

        msg = f"""-----TALK-----
        --update stances--
        {stances_text}
        --update colour_scales--
        {colour_scales_text}
        --update coming_outs--
        {coming_outs_text}
        --update my_tactics--
        {self.my_tactics.tactics}
        --statement--
        {statement}
        --------------"""
        log(self.index, [msg])
        log_talk(self.index, self.role, statement)

    # def vote(self) -> str:
    #     target_id = self.decide_vote()
    #     self.save_vote_log(target_id)

    #     data = {"agentIdx": target_id}
    #     return json.dumps(data, separators=(",", ":"))

    # def save_vote_log(self, target_id: int):
    #     log(self.index, [f"投票先を決定: 自分のid: {self.index}, target: {target_id}"])

    def update_stances(self):
        # スレッドプールエグゼキュータを使用して並列に処理
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 各スタンスの更新タスクをサブミット
            futures = [
                executor.submit(stance.update, self.day, self.talkHistory)
                for stance in self.stances
            ]
            # 全てのタスクが完了するのを待つ
            concurrent.futures.wait(futures)

    def update_colour_scales(self):
        # スレッドプールエグゼキュータを使用して並列に処理
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 各スタンスの更新タスクをサブミット
            futures = [
                executor.submit(colour_scale.update, self.day, self.talkHistory)
                for colour_scale in self.colour_scales
            ]
            # 全てのタスクが完了するのを待つ
            concurrent.futures.wait(futures)

    def update_coming_outs(self):
        # スレッドプールエグゼキュータを使用して並列に処理
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 各スタンスの更新タスクをサブミット
            futures = [
                executor.submit(coming_out.update, self.day, self.talkHistory)
                for coming_out in self.coming_outs
            ]
            # 全てのタスクが完了するのを待つ
            concurrent.futures.wait(futures)

    def update_my_tactics(self):
        self.my_tactics.update(
            self.day, self.stances, self.colour_scale, self.coming_outs
        )

    def generate_statement(self):
        return generate_statement(
            f"{int(self.index):02d}", self.role, self.talkHistory, self.my_tactics
        )

    # def decide_vote(self) -> int:
    #     return self.my_tactics.decide_vote_target(self.index, self.role, self.alive)

    def _get_formatted_agent_ids(self) -> list[str]:
        """
        エージェントIDのリストを整形された形式で取得する
        Returns:
            list[str]: 整形されたエージェントIDのリスト
        """
        statusMap = self.gameInfo["statusMap"]
        return [
            f"{util.get_index_from_name(agent_name=agent_id):02d}"
            for agent_id in statusMap.keys()
        ]

    def init_stances(self):
        """
        スタンス情報を初期化
        """
        self.stances = [
            Stance(f"{int(self.index):02d}", self.role, agent_id)
            for agent_id in self._get_formatted_agent_ids()
        ]

    def init_colour_scales(self):
        """
        カラースケール情報を初期化
        """
        self.colour_scales = [
            Colour_Scale(f"{int(self.index):02d}", self.role, agent_id)
            for agent_id in self._get_formatted_agent_ids()
        ]

    def init_coming_outs(self):
        """
        カミングアウト情報を初期化
        """
        self.coming_outs = [
            Coming_Out(f"{int(self.index):02d}", self.role, agent_id)
            for agent_id in self._get_formatted_agent_ids()
        ]

    def init_tactics(self):
        """
        initializeを受け取ったタイミングで実行
        """
        self.my_tactics = MyTactics(
            day=0,  # 初期化時は0日目
            my_agent_id=f"{int(self.index):02d}",
            my_agent_role=self.role,
            roleNumMap=self.gameSetting["roleNumMap"],
        )

    def hand_over(self, new_agent) -> None:
        super().hand_over(new_agent)
        new_agent.my_tactics = self.my_tactics
        new_agent.stances = self.stances
        new_agent.colour_scales = self.colour_scales
        new_agent.coming_outs = self.coming_outs
        new_agent.day = self.day
