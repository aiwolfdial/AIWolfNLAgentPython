def log(agent_id: int, msg_list: list[str]):
    """
    ログを出力

    TODO:
    - ログを消去する関数を作る
    """
    if type(agent_id) != int:
        agent_id = int(agent_id)

    with open(
        f"player_openai/dev_functions/logs/agent_{agent_id}_log.txt",
        "a",
        encoding="utf-8",
    ) as f:
        for msg in msg_list:
            print(msg, file=f)


def clear_log(agent_id: int):
    """
    ログを消去する
    """

    if type(agent_id) != int:
        agent_id = int(agent_id)

    filename = f"player_openai/dev_functions/logs/agent_{agent_id}_log.txt"

    with open(filename, "w", encoding="utf-8") as f:
        pass


def log_talk(agent_id: int, role: str, statement: str):

    if type(agent_id) != int:
        agent_id = int(agent_id)

    filename = "player_openai/dev_functions/logs/talk_history_log.txt"

    with open(filename, "a", encoding="utf-8") as f:
        msg = f"""
Agent[0{agent_id}] - role: {role}
{statement}
"""
        print(msg, file=f)
