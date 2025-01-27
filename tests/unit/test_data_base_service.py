import pytest
from sqlalchemy import inspect

from ..data.data_base_service import parametrize_create_tables_with_specific_models


class TestDataBaseService:

    def test_create_tables(self, db):
        """
        Тестирует создание таблиц в базе данных.

        :param db: Объект базы данных, в которой проверяется создание таблиц.
        :raises AssertionError: Если ожидаемые таблицы не созданы.
        """
        db.drop_tables()
        db.create_tables()
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        assert "users" in tables, "Таблица 'users' не создана"
        assert "reminders" in tables, "Таблица 'reminders' не создана"

    def test_drop_tables(self, db):
        """
        Проверяет удаление таблиц из базы данных.

        :param db: Объект базы данных для проверки операций удаления таблиц.
        :raises AssertionError: Если таблицы 'users' или 'reminders' не были удалены.
        """
        db.create_tables()
        db.drop_tables()
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        assert "users" not in tables, "Таблица 'users' не была удалена"
        assert "reminders" not in tables, "Таблица 'reminders' не была удалена"

    @pytest.mark.parametrize("models, excepted_tables, contex", parametrize_create_tables_with_specific_models)
    def test_create_tables_with_specific_models(self, db, models, excepted_tables, contex):
        """
        Тестирует создание таблиц на основе указанных моделей.

        :param db: База данных для выполнения операций.
        :param models: Модель или список моделей для создания таблиц.
        :param excepted_tables: Ожидаемые названия таблиц после выполнения.
        :param contex: Контекст выполнения теста, который может содержать исключение.
        """
        with contex:
            db.drop_tables()
            db.create_tables(models)
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            expected = [excepted_tables] if not isinstance(excepted_tables, (list, tuple)) else excepted_tables
            assert sorted(expected) == sorted(tables)
