from __future__ import annotations

import datetime
import multiprocessing
import multiprocessing.sharedctypes


class LogInfo:
    format = "%Y-%m-%d-%H-%M-%S-%f"
    encode = "utf-8"

    def __init__(self) -> None:
        self.__game_start_time = multiprocessing.sharedctypes.Array("c", 100)
        self.__log_num = multiprocessing.Value("i", 0)
        self.__log_times_num = multiprocessing.Value("i", 0)
        self.__log_prepare_done_num = multiprocessing.Value("i", 0)

    @property
    def game_start_time(self) -> str:
        return self.__game_start_time.value.decode()

    @game_start_time.setter
    def game_start_time(self, time: datetime.datetime) -> ValueError | None:
        if type(time) is not datetime.datetime:
            raise ValueError(time, "is not datetime.datetime")

        self.__game_start_time.value = bytes(
            time.strftime(LogInfo.format),
            LogInfo.encode,
        )

    @property
    def log_num(self) -> int:
        return self.__log_num.value

    def increment_log_num(self) -> None:
        self.__log_num.value += 1

    @property
    def log_times_num(self) -> int:
        return self.__log_times_num.value

    @log_times_num.setter
    def log_times_num(self, times: int) -> ValueError | None:
        if type(times) is not int:
            raise ValueError(times, "is not int")

        self.__log_times_num.value = times

    @property
    def log_prepare_done_num(self) -> int:
        return self.__log_prepare_done_num.value

    def increment_log_prepare_done_num(self) -> None:
        self.__log_prepare_done_num.value += 1

    def reset_params(self) -> None:
        self.log_times_num = 0
        self.__log_prepare_done_num.value = 0
