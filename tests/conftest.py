import pytest

from src.data_base.configuration.config import DataBaseConfig
from src.data_base.data_base_service import DataBaseService


@pytest.fixture(scope="function")
def db():
    """фикстура для тестового сервиса базы данных."""
    test_db_config = DataBaseConfig(url="sqlite:///:memory:")
    return DataBaseService(database_config=test_db_config)
