import os
import sys
from pathlib import Path
from subprocess import CalledProcessError, check_call

from loguru import logger

from thumbnail_generator_ubuntu.thumbgen import main

THIS_DIRECTORY = Path(__file__).parent

files = ["thumbnail_generator_ubuntu/", "tests/", "scripts.py"]


def thumbgen():
    main()


def fix():
    _call("black", files)


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
