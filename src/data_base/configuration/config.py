from dataclasses import dataclass


@dataclass
class DataBaseConfig:
    url: str
    echo: bool = False
    autocommit: bool = False
    autoflush: bool = False
