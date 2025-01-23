import pytest

from src.data_base.model import Users
from src.data_base.service_model.base_service import BaseCRUDService


# Успешное создание записи. Создание нескольких объектов. +
# Обработку ошибок (некорректные данные, дублирование уникальных полей).
# Работа с автоматически генерируемыми полями.
# Возврат созданного объекта.
# Обработку транзакций и откатов (rollback).

@pytest.fixture
def setup_users_table(db):
    """Фикстура для создания таблицы Users на чистой базе."""
    db.drop_tables()
    db.create_tables(Users)
    yield db


class TestUsersCRUDCreate:

    @pytest.mark.parametrize(
        "users_data, expected_count",
        [
            # Тест на создание одной записи
            ([{"nickname": "user1", "name": "Иван", "surname": "Иванов"}], 1),

            # Тест на создание нескольких записей
            ([
                 {"nickname": "user1", "name": "Иван", "surname": "Иванов"},
                 {"nickname": "user2", "name": "Алексей", "surname": "Петров"},
                 {"nickname": "user3", "name": "Мария", "surname": "Сидорова"}
             ], 3),
        ]
    )
    def test_create(self, setup_users_table, users_data, expected_count):
        """
        Тестирует создание пользователей в базе данных.

        :param setup_users_table: Фикстура для инициализации таблицы пользователей.
        :param users_data: Список данных пользователей для создания записей в таблице.
        :param expected_count: Ожидаемое количество записей в таблице после создания.
        :raises AssertionError: Если количество созданных записей или данные создаваемых пользователей не соответствуют ожидаемым.
        """
        with setup_users_table.session_scope() as session:
            base_serv = BaseCRUDService(session, Users)
            for user_data in users_data:
                new_users = base_serv.create(**user_data)
                assert new_users.nickname == user_data["nickname"]
                assert new_users.name == user_data["name"]
                assert new_users.surname == user_data["surname"]

            session.commit()

            saved_users = session.query(Users).all()
            assert len(saved_users) == expected_count

            for user_data in users_data:
                saved_user = session.query(Users).filter_by(nickname=user_data["nickname"]).first()
                assert saved_user is not None
                assert saved_user.name == user_data["name"]
                assert saved_user.surname == user_data["surname"]
