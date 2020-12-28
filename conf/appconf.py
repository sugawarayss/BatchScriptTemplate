import dataclasses
from typing import Final


@dataclasses.dataclass(frozen=True)
class AppConf:
    key: str = "hoge"
    key2: int = 1


