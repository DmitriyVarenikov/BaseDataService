from dataclasses import dataclass


@dataclass
class DataBaseConfig:
    url: str
    echo: bool = True
    autocommit: bool = False
    autoflush: bool = False
