import configparser
import datetime
from pathlib import Path
from typing import Callable

from utils import agent_util
from utils.log import Log
from utils.log_info import LogInfo


class AgentLog(Log):
    header_format = "-------------{header}-------------"
    small_header_format = "-------{header}-------"
    custom_response = "--------------{custom} RESPONSE--------------"

    def __init__(
        self,
        config: configparser.ConfigParser,
        agent_name: str,
        log_info: LogInfo,
    ) -> None:
        log_config_path = config.get("path", "log_config")
        if Path(log_config_path).exists():
            log_config = configparser.ConfigParser()
            log_config.read(log_config_path)
        else:
            raise FileNotFoundError(log_config_path, "設定ファイルが見つかりません")

        current_time = datetime.datetime.now()  # noqa: DTZ005

        if log_info.log_num % config.getint("agent", "num") == 0:
            log_info.game_start_time = current_time
        else:
            current_time = datetime.datetime.strptime(  # noqa: DTZ007
                log_info.game_start_time,
                LogInfo.format,
            )

        log_info.increment_log_num()

        self.is_write = log_config.getboolean("log", "write")
        self.log_dir_path = Path(log_config.get("path", "output_dir"))
        self.log_month_day_dir = Path.joinpath(
            self.log_dir_path,
            current_time.strftime("%m-%d"),
        )

        dir_num = 0
        if log_info.log_times_num == 0:
            if self.log_month_day_dir.exists():
                dir_num = (
                    len(
                        [
                            d.name
                            for d in self.log_month_day_dir.iterdir()
                            if d.is_dir()
                        ],
                    )
                    + 1
                )
            else:
                dir_num = 1
            log_info.log_times_num = dir_num
        else:
            dir_num = log_info.log_times_num

        self.log_times = Path.joinpath(self.log_month_day_dir, str(dir_num))
        self.log_file_path = Path.joinpath(
            self.log_times,
            current_time.strftime("%H-%M-%S-%f") + "_" + agent_name + ".log",
        )

        # load [log] flags
        self.log_flag_dict = {}  # key: func_name , value: flag
        self.log_flag_dict["get_info"] = log_config.getboolean("log", "get_info")
        self.log_flag_dict["initialize"] = log_config.getboolean("log", "initialize")
        self.log_flag_dict["talk"] = log_config.getboolean("log", "talk")
        self.log_flag_dict["vote"] = log_config.getboolean("log", "vote")

        if not self.is_write:
            return

        self.prepare_log_dir()

        super().__init__(filename=self.log_file_path, name=agent_name)

        log_info.increment_log_prepare_done_num()

        if log_info.log_prepare_done_num % config.getint("agent", "num") == 0:
            log_info.reset_params()

    @staticmethod
    def print_header_decorator(func: Callable) -> Callable:
        def _wrapper(self, *args, **kwargs) -> None:  # noqa: ANN001, ANN002, ANN003
            if not self.log_flag_dict.get(func.__name__, True) or not self.is_write:
                return None

            if kwargs.get("header") is not None:
                self.info(AgentLog.header_format.format(header=kwargs.get("header")))
            else:
                self.info(AgentLog.header_format.format(header=func.__name__))

            return func(self, *args, **kwargs)

        return _wrapper

    def prepare_log_dir(self) -> None:
        self.log_dir_path.mkdir(parents=True, exist_ok=True)
        self.log_month_day_dir.mkdir(parents=True, exist_ok=True)
        self.log_times.mkdir(parents=True, exist_ok=True)

    @print_header_decorator
    def get_info(self, get_info: map, request: str) -> None:
        self.info(get_info)
        self.info("Request:" + request)

    @print_header_decorator
    def initialize(self, role: str) -> None:
        self.info("ROLE:" + role)

    @print_header_decorator
    def talk(self, comment: str) -> None:
        self.info(msg=comment)

    @print_header_decorator
    def vote(self, vote_target: int) -> None:
        self.info("Vote: " + agent_util.agent_idx_to_agent(idx=vote_target))

    @print_header_decorator
    def divine(self, divine_target: int) -> None:
        self.info("Divine: " + agent_util.agent_idx_to_agent(idx=divine_target))

    @print_header_decorator
    def divine_result(self, divine_result: dict) -> None:
        self.info(divine_result)

    @print_header_decorator
    def attack(self, attack_target: int) -> None:
        self.info("Attack: " + agent_util.agent_idx_to_agent(idx=attack_target))

    @print_header_decorator
    def daily_finish(self) -> None:
        pass
