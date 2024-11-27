from __future__ import annotations

import configparser
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from utils.log_info import LogInfo

if TYPE_CHECKING:
    from configparser import ConfigParser

from time import sleep

from aiwolf_nlp_common import Action, util

import player
import utils

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def run_agent(
    idx: int,
    config: ConfigParser,
    log_info: LogInfo,
) -> None:
    sock = util.get_socket(inifile=config, name=config.get("agent", f"name{idx}"))
    name = config.get("agent", f"name{idx}")
    while True:
        try:
            sock.connect()
            logger.info("エージェント %s がゲームサーバに接続しました", name)
            break
        except Exception:  # noqa: BLE001
            sleep(15)
            logger.warning("エージェント %s がゲームサーバに接続できませんでした", name)
            logger.info("再接続を試みます")

    agent = player.agent.Agent(config=config, name=name, log_info=log_info)
    while not agent.is_finish:
        if len(agent.received) == 0:
            receive = sock.receive()
            if isinstance(receive, (str, list)):
                agent.parse_info(receive=receive)
        agent.get_info()
        message = agent.action()
        if Action.is_initialize(request=agent.protocol.request):
            agent = utils.agent_util.init_role(
                agent=agent,
                inifile=config,
                name=name,
                log_info=log_info,
            )
        if message != "":
            sock.send(message=message)

    sock.close()
    logger.info("エージェント %s とゲームサーバの接続を切断しました", name)


def execute(
    idx: int,
    config: ConfigParser,
    log_info: LogInfo,
) -> None:
    while True:
        for _ in range(config.getint("game", "num")):
            run_agent(
                idx=idx,
                config=config,
                log_info=log_info,
            )

        if not config.getboolean("connection", "keep_connection"):
            break


if __name__ == "__main__":
    config_path = "./src/res/config.ini"
    if Path(config_path).exists():
        config = configparser.ConfigParser()
        config.read(config_path)
        logger.info("設定ファイルを読み込みました")
    else:
        raise FileNotFoundError(config_path, "設定ファイルが見つかりません")
    log_info = LogInfo()

    execute(
        1,
        config,
        log_info,
    )
