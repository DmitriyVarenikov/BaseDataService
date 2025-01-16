import configparser
from enum import Enum

from .configuration.config import DataBaseConfig
from .types_db import DataBaseType
from .configuration.constrains import CONFIG_FILE



def load_config(database_type: DataBaseType, config_path:str = None) -> DataBaseConfig:

    if not isinstance(database_type, Enum):
        raise TypeError(f"Неверный тип базы данных {database_type}")

    if config_path is None:
        config_path = CONFIG_FILE
    config = configparser.ConfigParser()
    config.read(config_path)

    if database_type.value not in config:
        raise ValueError(f"Секция '{database_type.value}' не найдена в конфигурационном файле: {config_path}")

    if DataBaseType.URL.value not in config[database_type.value]:
        raise ValueError(f"Ключ '{DataBaseType.URL.value}' отсутствует в секции '{database_type.value}'")

    url = config[database_type.value][DataBaseType.URL.value]
    return DataBaseConfig(url)
