from player_openai.info_types import TalkHistory
from player_openai.langchain import OpenAIAgent

openai_agent = OpenAIAgent(temperature=1)

def get_colour_scale(
        my_agent_id: str,
        my_agent_role: str,
        target_agent_id: str,
        day_colour_scale: dict[int, str],
        talk_history: TalkHistory) -> str:
    """
    他のエージェントのスタンスをまとめる

    Args:
        my_agent_id (str): 自分のエージェントID
        my_agent_role (str): 自分の役職
        target_agent_id (str): 対象のエージェントID
        day_colour_scale (dict[int, str]): 日毎のグレー度合い
        talk_history (TalkHistory): 発言履歴
    
    Returns:
        str: その日の、この関数を呼び出した時点での対象エージェントのグレー度合い
    """
    
    system = """
あなたはAgent[{my_agent_id}]という名前で人狼ゲームをプレイしています。
あなたの役職は{my_agent_role}です。
"""

    template = """
# 指示
このプロンプトでは、人狼ゲームにおける特定のエージェント（Agent[{target_agent_id}]）の発言と行動、また占い結果などから、対象エージェントが市民陣営である確率がどれくらいかを判定します。

# 注意点
Agent[{target_agent_id}]がまだ発言、占いなどされていない場合、記録は行わないでください。その場合出力は空欄("")としてください。
範囲を持たせず、数字％の形で出力してください。（例：30%）

# タスク
対象エージェントAgent[{target_agent_id}]が他のエージェントに関してどのような発言をしているか、どのような役職をカミングアウトしているか、また占い師（SEER）にどのように占われているかに注目して、対象エージェントが市民陣営である確率がどれくらいかを判定してください。
例えば、占い師とカミングアウトしている人が一人の場合は、市民陣営である確率は、{"カミングアウトした占い師": 100%, "'HUMAN'と占われたエージェント": 100%, "'WEREWOLF'と占われたエージェント": 0%, "'WEREWOLF'が確定していない状況で、占われていないエージェント": 
66%}となる。
例えば、占い師とカミングアウトしている人が二人でどちらも生きている場合は、市民陣営である確率は、{"どちらにも'HUMAN'と占われたエージェント": 100%, "どちらにも'WEREWOLF'と占われたエージェント": 0%, "他のエージェント": 20%から25%}

# 出力形式
- 市民陣営である確率: [対象エージェントが市民陣営である確率を0%から100%で記してください。]

# データ
- 発言履歴
{talk_history}
"""

    try:
        input = {"my_agent_id": my_agent_id, "my_agent_role": my_agent_role, "target_agent_id": target_agent_id, "day_colour_scale": get_str_day_colour_scale(day_colour_scale), "talk_history": get_str_talk_history(talk_history)}

        output = openai_agent.chat(system, template, input)

        return output
    except Exception as e:
        print("error:", e)
        return ""

def get_str_day_colour_scale(day_colour_scale: dict[int, str]) -> str:
    return str(day_colour_scale)

def get_str_talk_history(talk_history: TalkHistory) -> str:
    # MEMO: f-stringで書きたいが、[]をエスケープする必要があるため、+演算子で結合
    return "\n".join(["Agent[0" + str(talk["agent"]) + "]\n" + talk["text"] for talk in talk_history])