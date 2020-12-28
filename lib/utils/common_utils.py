import argparse
import json
from os import environ, uname
import logging
from logging import Logger, config
from typing import Optional, Dict
from pathlib import Path
import sys
from typing import Tuple, Union, List


class RunningEnvironmentError(Exception):
    pass


def get_target_env_conf_path(is_log_conf=False, log: Logger = None) -> str:
    """
    スクリプトの起動オプションに応じてconfファイルのパスを返す
    :param: is_log_conf logConfが欲しいかフラグ
    :return: confファイルのパス
    """
    parser = argparse.ArgumentParser(description="TRC Project")
    parser.add_argument("-e", "--env", help="specified env [ --env dev | --env prod ]")
    args = parser.parse_args()
    if args.env == "dev":
        if is_log_conf:
            return environ["DEV_LOG_CONFIG_PATH"]
        else:
            return environ["DEV_ENV_CONF_PATH"]
    else:
        # 開発マシンから本番環境の操作を防止する
        if uname()[1] == environ["PROD_HOST_NAME"]:
            if is_log_conf:
                return environ["PROD_LOG_CONFIG_PATH"]
            else:
                return environ["PROD_ENV_CONF_PATH"]
        else:
            raise RunningEnvironmentError("prod mode can run script at production server only", uname()[1])


def load_env_conf(path: Optional[str], log: Logger = None) -> Optional[Dict]:
    """
    conf.jsonをパースして返す
    :return:
    """
    conf_path = get_target_env_conf_path(is_log_conf=False)
    if path is not None:
        conf_path = path
    with open(conf_path, "r") as f:
        return json.load(f)


def load_app_conf(log: Logger = None) -> Dict:
    json_path = get_target_env_conf_path(is_log_conf=False)
    # TODO:エラー処理
    with open(json_path, "r") as f:
        return json.load(f)


def setup_logging(log_path: Union[str, Path]) -> Logger:
    # if type(root_path) is str:
    #     root_path = Path(root_path)
    if type(log_path) is str:
        log_path = Path(log_path)

    # print(f"root: {root_path}")
    print(f"log_conf: {log_path}")

    # log_conf_path = root_path / log_path
    log_conf_path = log_path
    print(f"log_conf: {log_conf_path}")
    config.fileConfig(str(log_conf_path))
    logger = logging.getLogger()
    logger.info("logger init")
    return logger


def get_options() -> Tuple[str, Union[bool, List]]:
    """
    実行時の引数を解析します
    :return str groupname タスクグループ名
    :return list|False taskname タスク
    """
    parser = argparse.ArgumentParser(prog='RUN TASK', description='Run Octoparseタスク')
    parser.add_argument('-g', '--groupname', type=str, nargs=1, required=True)  # グループ名は必須
    parser.add_argument('-t', '--taskname', type=str, nargs='+')  # タスク名は必須ではない
    parge_args = parser.parse_args()

    groupname = parge_args.groupname[0]
    # False の可能性を洗い出して、全部Trueであれば、実行したタスクのリストを代入. 常にリストが入る.
    taskname = parge_args.taskname is not None and len(
        parge_args.taskname) != 0 and parge_args.taskname[0] != '' and parge_args.taskname
    return groupname, taskname


def get_platform() -> str:
    """
    プラットフォーム名を返す
    (Solaris/FreeBSD/AIX/WindowsSubsystemLinux/Linux/Windows/CygwinOnWindows/MacOS/Unknown)
    :return:
    """
    sys_platform_str: str = sys.platform
    if sys_platform_str.startswith('sunos'):
        return "Solaris"
    elif sys_platform_str.startswith('freebsd'):
        return "FreeBSD"
    elif sys_platform_str.startswith('aix'):
        return "AIX"
    elif sys_platform_str.startswith('linux2'):
        return "WSL"
    elif sys_platform_str.startswith('linux'):
        return "Linux"
    elif sys_platform_str.startswith('win32'):
        return "Windows"
    elif sys_platform_str.startswith('cygwin'):
        return "Windows/Cygwin"
    elif sys_platform_str.startswith('darwin'):
        return "MacOS"
    else:
        return "Unknown"
