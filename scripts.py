import os
import sys
from pathlib import Path
from subprocess import CalledProcessError, check_call

from loguru import logger

THIS_DIRECTORY = Path(__file__).parent

files = ["thumbgen/", "tests/", "scripts.py"]


def fix():
    _call("isort", ["-rc", "-l 120"] + files)
    _call("black", files)
    _call("flake8", files)


def _call(cmd, options=[]) -> None:
    command = cmd.split(" ") + options
    logger.info(">>>>>>>>     {}".format(" ".join(command)))
    try:
        os.chdir(THIS_DIRECTORY)
        check_call(command)
    except CalledProcessError as ex:
        print(f"[FAIL]  {ex}")
        sys.exit(2)
    logger.info("<<<<<<<<<< ")
