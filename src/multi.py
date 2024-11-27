import configparser
import logging
import multiprocessing
from pathlib import Path

import main
from utils.log_info import LogInfo

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")

    config_path = "./src/res/config.ini"
    if Path(config_path).exists():
        config = configparser.ConfigParser()
        config.read(config_path)
        logger.info("設定ファイルを読み込みました")
    else:
        raise FileNotFoundError(config_path, "設定ファイルが見つかりません")
    log_info = LogInfo()

    agent_num = int(config.get("agent", "num"))
    logger.info("エージェント数: %d", agent_num)

    processes = []
    for i in range(agent_num):
        process = multiprocessing.Process(
            name="p" + str(i + 1),
            target=main.execute,
            args=(
                i + 1,
                config,
                log_info,
            ),
        )
        processes.append(process)
        process.start()
        logger.info("エージェント %d を起動しました", i + 1)

    for process in processes:
        process.join()
