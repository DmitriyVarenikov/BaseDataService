import configparser
from enum import Enum

from src.data_base.configuration.config import DataBaseConfig
from src.data_base.configuration.constrains import CONFIG_FILE


class DataBaseType(Enum):
    SQLite = "sqlite"
    SQLite_test = "sqlite_test"
    PostgreSQL = "postgresql"
    URL = "url"

def load_config(database_type: DataBaseType, config_path:str = None) -> DataBaseConfig:

    if not isinstance(database_type, Enum):
        raise TypeError(f"Неверный тип базы данных {database_type}")

    if config_path is None:
        config_path = CONFIG_FILE
    config = configparser.ConfigParser()
    config.read(config_path)

    if database_type.value not in config:
        raise ValueError(f"Секция '{database_type.value}' не найдена в конфигурационном файле: {config_path}")

    conf_keys = config[database_type.value]
    kwargs = {k: conf_keys[k] for k in conf_keys}
    return DataBaseConfig(**kwargs)
