import pytest
from sqlalchemy import inspect
from contextlib import nullcontext

from src.data_base.model import Users, Reminders



class TestDataBaseService:

    def test_create_tables(self, db):
        """Проверка создания таблиц."""
        db.drop_tables()
        db.create_tables()
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        assert "users" in tables, "Таблица 'users' не создана"
        assert "reminders" in tables, "Таблица 'reminders' не создана"

    def test_drop_tables(self, db):
        """Проверка удаления таблиц."""
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
        ("sdfsdf", ["users", "reminders"], pytest.raises(TypeError))
    ])
    def test_create_tables_with_specific_models(self, db, models, excepted_tables, contex):
        with contex:
            db.drop_tables()
            db.create_tables(models)
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            expected = [excepted_tables] if not isinstance(excepted_tables, (list, tuple)) else excepted_tables
            assert sorted(expected) == sorted(tables)
