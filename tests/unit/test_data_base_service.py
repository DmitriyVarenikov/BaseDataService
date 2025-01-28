import pytest
from sqlalchemy import inspect

from ..data.data_base_service import parametrize_create_tables_with_specific_models


class TestDataBaseService:

    def test_create_tables(self, table_manager, db_engine):
        """
        Метод для тестирования процесса создания таблиц.

        :param table_manager: Объект, управляющий таблицами.
        :param db_engine: Объект подключения к базе данных.
        """
        table_manager.drop_tables()
        table_manager.create_tables()
        inspector = inspect(db_engine)
        tables = inspector.get_table_names()
        assert "users" in tables, "Таблица 'users' не создана"
        assert "reminders" in tables, "Таблица 'reminders' не создана"

    def test_drop_tables(self, table_manager, db_engine):
        """
        Тестирует удаление таблиц из базы данных.

        :param table_manager: Объект для управления таблицами.
        :param db_engine: Движок базы данных, используемый для подключения.
        """
        table_manager.create_tables()
        table_manager.drop_tables()
        inspector = inspect(db_engine)
        tables = inspector.get_table_names()
        assert "users" not in tables, "Таблица 'users' не была удалена"
        assert "reminders" not in tables, "Таблица 'reminders' не была удалена"

    @pytest.mark.parametrize("models, excepted_tables, contex", parametrize_create_tables_with_specific_models)
    def test_create_tables_with_specific_models(self, table_manager, db_engine, models, excepted_tables, contex):
        """
        Тест проверяет процесс создания таблиц в базе данных для заданных моделей.

        :param models: Список моделей, для которых необходимо создать таблицы.
        :param excepted_tables: Ожидаемый список названий таблиц после создания.
        :param contex: Контекст выполнения теста.
        """
        with contex:
            table_manager.drop_tables()
            table_manager.create_tables(models)
            inspector = inspect(db_engine)
            tables = inspector.get_table_names()
            expected = [excepted_tables] if not isinstance(excepted_tables, (list, tuple)) else excepted_tables
            assert sorted(expected) == sorted(tables)
