import datetime
import os
from logging import DEBUG, INFO, FileHandler, Formatter, StreamHandler, getLogger

import colorlog

FolderYear = datetime.datetime.now().strftime("%Y")
FolderDate = datetime.datetime.now().strftime("%m-%d")
LogFileName = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

LOG_FILE_PATH = f".log/{FolderYear}/{FolderDate}/{LogFileName}"
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)


logger = getLogger(__name__)
logger.setLevel(INFO)

stream = StreamHandler()
stream.setLevel(INFO)
stream_format = colorlog.ColoredFormatter(
    "%(asctime)s | %(log_color)s%(levelname)-8s%(reset)s | "
    "%(funcName)-15s | %(message)s",
    datefmt="%H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)
stream.setFormatter(stream_format)
logger.addHandler(stream)


file = FileHandler(LOG_FILE_PATH)
file.setLevel(DEBUG)
file_formatter = Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s"
)
file.setFormatter(file_formatter)
logger.addHandler(file)
