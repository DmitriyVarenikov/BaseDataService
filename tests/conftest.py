import pytest

from src.data_base.configuration.config import DataBaseConfig
from src.data_base.data_base_service import DataBaseService
from src.data_base.engine import DatabaseEngine
from src.data_base.table_manager import TableManager


@pytest.fixture(scope="session")
def db_config():
    """
    Фикстура для конфигурации базы данных.

    :return: Конфигурация базы данных.
    """
    return DataBaseConfig(url="sqlite:///:memory:")


@pytest.fixture(scope="session")
def db_engine(db_config):
    """
    Создает и возвращает экземпляр объекта подключения к базе данных.

    :param db_config: Конфигурация параметров базы данных.
    """
    return DatabaseEngine(db_config.url, db_config.echo).get_engine()


@pytest.fixture(scope="session")
def table_manager(db_engine):
    """
    Инициализирует фикстуру для управления таблицами в базе данных.

    :param db_engine: Объект подключения к базе данных.
    """
    return TableManager(db_engine)


@pytest.fixture(scope="session")
def db_service(db_config, db_engine):
    """
    Создает и возвращает экземпляр сервиса базы данных для использования в тестах.

    :param db_config: Конфигурация базы данных.
    :param db_engine: Объект движка базы данных.
    """
    return DataBaseService(database_config=db_config, engine=db_engine)


@pytest.fixture
def db_session(db_service):
    """
    Создает фикстуру для предоставления сессии базы данных.
    Автокомиты отключены.
    :param db_service: Сервис для работы с базой данных.
    """
    with db_service.session_scope(commit=False) as session:
        yield session
