class Base_Talk_Starategy:
    STRATEGIES = {
        "Day01": {
            "VILLAGER": {
                "NO_SEER_COMING_OUT": {"占い師がカミングアウトするように促す"},
                "ONE_SEER_COMING_OUT": {
                    "占い師を信用し、占い師が'WEREWOLF'と判定した人に投票するように、'HUMAN'と判定した人に投票しないように促す"
                },
                "TWO_SEER_COMING_OUT": {"できるだけ処刑されないように、様子を見る"},
            },
            "WEREWOLF": {
                "NO_SEER_COMING_OUT": {"できるだけ処刑されないように、様子を見る"},
                "ONE_SEER_COMING_OUT": {
                    "対抗で占い師とカミングアウトする。占い師が占ったエージェントとは別のエージェントの占い結果を共有する。相手の占い結果が'HUMAN'なら同じく'HUMAN'、'WEREWOLF'なら同じく'WEREWOLF'と占う"
                },
                "TWO_SEER_COMING_OUT": {"できるだけ処刑されないように、様子を見る"},
            },
            "POSSESED": {
                "NO_SEER_COMING_OUT": {"できるだけ処刑されないように、様子を見る"},
                "ONE_SEER_COMING_OUT": {
                    "対抗で占い師とカミングアウトする。占い師が占ったエージェントとは別のエージェントの占い結果を共有する。相手の占い結果が'HUMAN'なら同じく'HUMAN'、'WEREWOLF'なら同じく'WEREWOLF'と占う"
                },
                "TWO_SEER_COMING_OUT": {"できるだけ処刑されないように、様子を見る"},
            },
            "SEER": {
                "NO_SEER_COMING_OUT": {
                    "できるだけ早く自分が占い師だとカミングアウトし、占い結果を共有する。"
                },
                "ONE_SEER_COMING_OUT": {
                    "まだカミングアウトしていない場合は、できるだけ早く自分が占い師だとカミングアウトし、占い結果を共有する。"
                },
                "TWO_SEER_COMING_OUT": {
                    "まだカミングアウトしていない場合は、できるだけ早く自分が占い師だとカミングアウトし、占い結果を共有する。"
                },
            },
        }
    }
