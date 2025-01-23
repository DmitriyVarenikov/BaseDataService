import pytest
from sqlalchemy import inspect
from contextlib import nullcontext

from src.data_base.model import Users, Reminders



class TestDataBaseService:

    def test_create_tables(self, db):
        """
        Тест проверяет процесс создания таблиц в базе данных.

        Аргументы:
        db: Объект базы данных, над которой проводятся операции.
        """
        db.drop_tables()
        db.create_tables()
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        assert "users" in tables, "Таблица 'users' не создана"
        assert "reminders" in tables, "Таблица 'reminders' не создана"

    def test_drop_tables(self, db):
        """
        Тест проверяет успешное удаление таблиц в базе данных.

        Параметры:
        db (объект базы данных): Экземпляр базы данных, используемый для теста.
        """
        db.create_tables()
        db.drop_tables()
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        assert "users" not in tables, "Таблица 'users' не была удалена"
        assert "reminders" not in tables, "Таблица 'reminders' не была удалена"

    @pytest.mark.parametrize("models, excepted_tables, contex", [
        (Users, "users", nullcontext()),
        (Reminders, "reminders", nullcontext()),
        ([Users, Reminders], ["users", "reminders"], nullcontext()),
        (None, ["users", "reminders"], nullcontext()),
        ("...", ["users", "reminders"], pytest.raises(TypeError))
    ])
    def test_create_tables_with_specific_models(self, db, models, excepted_tables, contex):
        """
        Тест проверяет создание таблиц для указанных моделей в базе данных.

        Параметры:
        models: Модель или список моделей, для которых создаются таблицы.
        excepted_tables: Ожидаемые названия таблиц, соответствующие переданным моделям.
        contex: Контекст выполнения теста, указывающий на возможные исключения или отсутствие их.
        """
        with contex:
            db.drop_tables()
            db.create_tables(models)
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            expected = [excepted_tables] if not isinstance(excepted_tables, (list, tuple)) else excepted_tables
            assert sorted(expected) == sorted(tables)
