from player_openai.langchain import OpenAIAgent
from player_openai.info_types import TalkHistory
from player_openai.my_tactics import MyTactics

openai_agent = OpenAIAgent(temperature=1)


def generate_statement(
    my_agent_id: str,
    my_agent_role: str,
    talk_history: TalkHistory,
    my_tactics: MyTactics,
) -> str:
    """
    実際の発言を出力
    """

    system = """
あなたはAgent[{my_agent_id}]という名前で人狼ゲームをプレイしています。
あなたの役職は{my_agent_role}です。

"""

    template = """
# 指示
あなたは人狼ゲームをプレイしており、最新の戦略を踏まえた発言を生成することが目的です。直前の会話内容と一致し、かつ戦略的な意図を持った発言を作成してください。

# 注意点
- 出力はそのまま発言として使用されるため、発言以外の情報は含めないでください。
- 発言は簡潔かつ明確に、ゲーム内での自然な会話として整理してください。

# タスク
1. 直前の会話内容を分析し、そのトピックやトーンに基づいて発言を構築します。
2. あなたの戦略に基づいて、どのプレイヤーにどのようなメッセージを伝えるかを決定します。
3. 会話が自然であるように、過去の戦略や会話履歴から適切な情報を引用または参照し、新しい発言を形成します。

# データ
- 最新の戦略: {my_tactics}
- 直前の会話履歴: {talk_history}
"""

    try:
        input = {
            "my_agent_id": my_agent_id,
            "my_agent_role": my_agent_role,
            "talk_history": get_str_talk_history(talk_history),
            "my_tactics": get_str_my_tactics(my_tactics),
        }

        output = openai_agent.chat(system, template, input)
        return output
    except Exception as e:
        print(e)
        return "発言の生成に失敗しました"


def get_str_my_tactics(my_tactics: MyTactics):
    my_day_tactics: dict[int, str] = my_tactics.tactics
    return " ".join(
        [f"day: {day}, tactic: {tactic}" for day, tactic in my_day_tactics.items()]
    )


def get_str_talk_history(talk_history: TalkHistory) -> str:
    # MEMO: f-stringで書きたいが、[]をエスケープする必要があるため、+演算子で結合
    return "\n".join(
        [str(talk["agent"]) + "]\n" + talk["text"] for talk in talk_history]
    )
