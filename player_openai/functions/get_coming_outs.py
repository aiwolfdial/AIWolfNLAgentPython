from player_openai.info_types import TalkHistory
from player_openai.langchain import OpenAIAgent

openai_agent = OpenAIAgent(temperature=1)

def get_coming_outs(
        my_agent_id: str,
        my_agent_role: str,
        target_agent_id: str,
        day_coming_outs: dict[int, str],
        talk_history: TalkHistory) -> str:
    """
    他のエージェントのスタンスをまとめる

    Args:
        my_agent_id (str): 自分のエージェントID
        my_agent_role (str): 自分の役職
        target_agent_id (str): 対象のエージェントID
        day_coming_outs (dict[int, str]): 日毎のカミングアウト
        talk_history (TalkHistory): 発言履歴
    
    Returns:
        str: その日の、この関数を呼び出した時点での対象エージェントのスタンス
    """
    
    system = """
あなたはAgent[{my_agent_id}]という名前で人狼ゲームをプレイしています。
あなたの役職は{my_agent_role}です。
"""

    template = """
# 指示
このプロンプトでは、人狼ゲームにおける特定のエージェント（Agent[{target_agent_id}]）の発言と行動から、対象エージェントが何らかの役職をカミングアウト（自白）しているかどうかを記録します。

# 注意点
Agent[{target_agent_id}]がまだ発言していない場合、記録は行わないでください。その場合出力は空欄("")としてください。
明確にカミングアウトしていない場合は、空欄のまま出力してください。

# タスク
対象エージェントAgent[{target_agent_id}]が他のエージェントに関してどのような発言をしているかに注目し、明確に役職をカミングアウトしているかどうか判定してください。

# 出力形式
- 役職カミングアウト: [対象エージェントがカミングアウトした役職（"WEREWOLF", "VILLAGER", "POSSESED", "SEER", ""のいずれか）を記してください。]

# データ
- 発言履歴
{talk_history}
"""

    try:
        input = {"my_agent_id": my_agent_id, "my_agent_role": my_agent_role, "target_agent_id": target_agent_id, "day_coming_outs": get_str_day_coming_outs(day_coming_outs), "talk_history": get_str_talk_history(talk_history)}

        output = openai_agent.chat(system, template, input)

        return output
    except Exception as e:
        print("error:", e)
        return ""

def get_str_day_coming_outs(day_coming_outs: dict[int, str]) -> str:
    return str(day_coming_outs)

def get_str_talk_history(talk_history: TalkHistory) -> str:
    # MEMO: f-stringで書きたいが、[]をエスケープする必要があるため、+演算子で結合
    return "\n".join(["Agent[0" + str(talk["agent"]) + "]\n" + talk["text"] for talk in talk_history])