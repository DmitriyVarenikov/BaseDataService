import pytest
from sqlalchemy import inspect
from sqlalchemy.testing.plugin.plugin_base import config
import os

from src.data_base.data_base_service import DataBaseService
from src.data_base.types_db import DataBaseType
from src.data_base.configuration.config import DataBaseConfig
from src.data_base.config_loader import load_config

@pytest.fixture
def test_db():
    """Фикстура для тестирования SQLite в памяти."""
    config_path = os.path.join(os.path.dirname(__file__), "../", "src", "data_base", "config.ini")
    config_path = os.path.abspath(config_path)
    data_base_config = load_config(DataBaseType.SQLite_test, config_path)
    return DataBaseService(data_base_config)

def test_create_tables(test_db):
    """Проверка создания таблиц."""

    test_db.create_tables()
    inspector = inspect(test_db.engine)
    tables = inspector.get_table_names()

    # Проверяем, что таблицы созданы
    assert "users" in tables, "Таблица 'users' не создана"
    assert "reminders" in tables, "Таблица 'reminders' не создана"
