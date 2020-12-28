from pathlib import Path
import os
from typing import Final, Union


PROJECT_ROOT: Final[Path] = Path(os.path.dirname(__file__)).parents[1]


def check_exist(target_path: Union[Path, str]) -> Union[Path, str]:
    if isinstance(target_path, str):
        tmp_path = Path(target_path)
    else:
        tmp_path = target_path

    if not tmp_path.exists():
        tmp_path.mkdir(parents=True)
    return target_path


def get_project_root() -> Path:
    return PROJECT_ROOT


def get_pdf_path() -> Path:
    return check_exist(PROJECT_ROOT / 'PDF')


def get_config_path() -> Path:
    return check_exist(PROJECT_ROOT / 'conf')


def get_credential_path() -> Path:
    return check_exist(PROJECT_ROOT / 'conf/credential')


def get_data_path() -> Path:
    return check_exist(PROJECT_ROOT / 'data')


def get_keyword_path() -> Path:
    return check_exist(PROJECT_ROOT / 'data/extraction_keywords')


def get_log_path() -> Path:
    return check_exist(PROJECT_ROOT / 'log')


def get_output_path() -> Path:
    return check_exist(PROJECT_ROOT / 'output')


def get_output_child(pref: str, municipality: str, peryl: str) -> Path:
    tmp = get_output_path()
    return check_exist(tmp / pref / municipality / peryl)


def get_pickle_path() -> Path:
    return check_exist(PROJECT_ROOT / 'data/pickles')


def get_home_path():
    return os.path.expanduser('~')
