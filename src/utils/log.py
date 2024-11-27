from __future__ import annotations

import logging
import logging.handlers
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class Log:
    encoding: str = "utf-8"

    def __init__(self, filename: Path, name: str) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(
            filename,
            mode="w",
            encoding=Log.encoding,
        )
        self.handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(self.handler)

    def debug(self, msg: object) -> None:
        self.logger.debug(msg)

    def info(self, msg: object) -> None:
        self.logger.info(msg)

    def warning(self, msg: object) -> None:
        self.logger.warning(msg)

    def error(self, msg: object) -> None:
        self.logger.error(msg)

    def exception(self, msg: object) -> None:
        self.logger.exception(msg)

    def critical(self, msg: object) -> None:
        self.logger.critical(msg)

    def close(self) -> None:
        self.logger.removeHandler(self.handler)
        self.handler.close()
        logging.shutdown()
