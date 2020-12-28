from logging import Logger
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
from lib.utils.path_utils import get_config_path
from lib.utils.common_utils import setup_logging
from conf.appconf import AppConf


def main():
    logger: Logger = setup_logging(get_config_path() / "dev_logging.conf")
    try:
        hoge = AppConf.key
        print(hoge)
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
