import logging
import sys
from colorama import Fore, Back, Style, init as colorama_init

colorama_init(autoreset = True)

SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")


def success(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)

logging.Logger.success = success


class ColorFormatter(logging.Formatter):
    COLORS = {
        'INFO': f"{Fore.WHITE}[{Fore.BLUE}INFO{Fore.WHITE}]{Style.RESET_ALL}",
        'SUCCESS': f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}SUCCESS{Fore.WHITE}]{Style.RESET_ALL}",
        'WARNING': f"{Fore.WHITE}[{Fore.YELLOW}WARNING{Fore.WHITE}]{Style.RESET_ALL}",
        'ERROR': f"{Fore.WHITE}[{Back.RED}ERROR{Back.RESET}]{Style.RESET_ALL}",
        'CRITICAL': f"{Fore.WHITE}[{Back.RED}CRITICAL{Back.RESET}]{Style.RESET_ALL}",
    }

    def format(self, record):
        label = self.COLORS.get(record.levelname, f"[{record.levelname}]")
        record.levelname = label
        return super().format(record)


class Logger:
    def __init__(self, name: str | None = None, filename: str | None = None, stream: bool = True, color: bool = True):
        self._log = logging.getLogger(name)
        self._log.setLevel(logging.INFO)
        self._log.propagate = False  # avoids duplicate logs from root

        formatter = ColorFormatter("%(asctime)s - %(levelname)s\t - %(message)s", "%Y-%m-%d %H:%M") if color \
                    else logging.Formatter("%(asctime)s - [%(levelname)s]\t - %(message)s", "%Y-%m-%d %H:%M")

        if stream:
            sh = logging.StreamHandler(sys.stdout)
            sh.setFormatter(formatter)
            self._log.addHandler(sh)

        if filename:
            fh = logging.FileHandler(filename)
            fh.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s", "%Y-%m-%d %H:%M"))
            self._log.addHandler(fh)

    def set_level(self, level: int):
        self._log.setLevel(level)

    def success(self, msg: object):  # Custom level for success
        self._log.success(msg)

    def info(self, msg: object):
        self._log.info(msg)

    def warn(self, msg: object):
        self._log.warning(msg)

    def error(self, msg: object):
        self._log.error(msg)

    def critical(self, msg: object):
        self._log.critical(msg)
