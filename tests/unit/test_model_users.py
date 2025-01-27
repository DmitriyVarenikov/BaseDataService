import pytest

from sqlalchemy.exc import IntegrityError

from src.data_base.model import Users
from src.data_base.service_model.base_service import BaseCRUDService
from ..data.data_model_users import parametrize_create, parametrize_duplicate_name, parametrize_invalid_user_data


# Успешное создание записи. Создание нескольких объектов. +
# Обработку ошибок (некорректные данные, дублирование уникальных полей). +
# Работа с автоматически генерируемыми полями. +
# Возврат созданного объекта. +
# Обработку транзакций и откатов (rollback). +

@pytest.fixture
def setup_users_table(db):
    """Фикстура для создания таблицы Users на чистой базе."""
    db.drop_tables()
    db.create_tables(Users)
    yield db


@pytest.fixture
def db_session(setup_users_table):
    """
    Создает фикстуру для сессии базы данных.

    Для тестов коммит внутри сессии отключен.

    :param setup_users_table: Фикстура для настройки таблицы пользователей.
    """
    with setup_users_table.session_scope(commit=False) as session:
        yield session


class TestUsersCRUDCreate:

    @pytest.mark.parametrize(
        "users_data, expected_count", parametrize_create)
    def test_create(self, db_session, users_data, expected_count):
        base_serv = BaseCRUDService(db_session, Users)
        for user_data in users_data:
            new_users = base_serv.create(**user_data)
            assert new_users.nickname == user_data["nickname"]
            assert new_users.name == user_data["name"]
            assert new_users.surname == user_data["surname"]

        db_session.flush()

        saved_users = db_session.query(Users).all()
        assert len(saved_users) == expected_count

        for user_data in users_data:
            saved_user = db_session.query(Users).filter_by(nickname=user_data["nickname"]).first()
            assert saved_user is not None
            assert saved_user.name == user_data["name"]
            assert saved_user.surname == user_data["surname"]
            assert saved_user.id is not None, "Поле id должно быть сгенерировано"
            assert saved_user.created_at is not None, "Поле created_at должно быть сгенерировано"

    @pytest.mark.parametrize("users_data", parametrize_duplicate_name)
    def test_create_duplicate_nickname(self, db_session, users_data):
        """
        Тест проверяет создание записи пользователя с дублирующимся никнеймом.

        :param users_data: Данные пользователей, включающие оригинальный и дублирующийся никнейм.
        """
        base_serv = BaseCRUDService(db_session, Users)
        base_serv.create(**users_data[0])
        db_session.flush()

        # проверяем, что первый пользователь сохранён
        saved_users = db_session.query(Users).all()
        assert len(saved_users) == 1  # сохраняем только уникальные записи
        assert saved_users[0].nickname == users_data[0]["nickname"]

        # Проверяем, что создание дубликата вызывает IntegrityError
        with pytest.raises(IntegrityError):
            base_serv.create(**users_data[1])
            db_session.flush()

    @pytest.mark.parametrize("users_data", parametrize_invalid_user_data)
    def test_invalid_user_data(self, db_session, users_data):
        """
        Тест проверяет обработку некорректных данных пользователей и выбрасывание исключений.

        :param db_session: Сессия базы данных.
        :param users_data: Набор данных с некорректной информацией о пользователях.
        """
        base_serv = BaseCRUDService(db_session, Users)
        for user_data in users_data:
            with pytest.raises(IntegrityError):
                base_serv.create(**user_data)
                db_session.flush()
            db_session.rollback()
