import pytest

from sqlalchemy.exc import IntegrityError

from src.data_base.model import Users
from src.data_base.service_model.base_service import BaseCRUDService
from ..data.data_model_users import parametrize_create, parametrize_duplicate_name, parametrize_invalid_user_data, \
    parametrize_filter_single_field, parametrize_with_filter_multiple_fields


# Успешное создание записи. Создание нескольких объектов. +
# Обработку ошибок (некорректные данные, дублирование уникальных полей). +
# Работа с автоматически генерируемыми полями. +
# Возврат созданного объекта. +
# Обработку транзакций и откатов (rollback). +

@pytest.fixture
def setup_users_table(table_manager):
    """Фикстура для создания таблицы Users на чистой базе."""
    table_manager.drop_tables()
    table_manager.create_tables(Users)


@pytest.mark.usefixtures("setup_users_table")
class TestUsersCRUDCreate:

    @pytest.mark.parametrize(
        "users_data, expected_count", parametrize_create)
    def test_create(self, db_session, users_data, expected_count):
        """
        Тестирует создание пользователей с использованием сервиса BaseCRUDService.

        :param users_data: Данные пользователей для создания.
        :param expected_count: Ожидаемое количество созданных пользователей.
        """
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
        Тест проверяет возможность создания дубликата никнейма пользователя.

        :param users_data: Данные о пользователях, где один из записей содержит дублирующийся никнейм.
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
        Тест проверяет обработку недопустимых данных пользователей и гарантирует возникновение исключения при попытке их добавления в базу данных.

        :param db_session: Текущая сессия базы данных.
        :param users_data: Набор данных пользователей, которые считаются недопустимыми.
        """
        base_serv = BaseCRUDService(db_session, Users)
        for user_data in users_data:
            with pytest.raises(IntegrityError):
                base_serv.create(**user_data)
                db_session.flush()
            db_session.rollback()


#  Чтение всех записей в таблице. +
#  Чтение записей по одному полю (фильтрация).
#  Чтение записей по нескольким полям (сложная фильтрация).
#  Чтение записей с сортировкой по одному полю.
#  Чтение записей с сортировкой по нескольким полям.
#  Чтение записей с лимитом (ограничение количества).
#  Чтение записей с оффсетом (пагинация).
#  Чтение записей с комбинацией фильтрации, сортировки и лимита.
#  Чтение записей, когда в таблице нет данных.
#  Чтение записей, когда фильтр не соответствует ни одной записи.


@pytest.mark.usefixtures("setup_users_table")
class TestUsersCRUDRead:

    @pytest.mark.parametrize("users_data, expected_count", parametrize_create)
    def test_all(self, db_session, users_data, expected_count):
        """
        Тестирует метод создания и чтения пользователей, проверяя их количество и тип.

        :param db_session: Сессия базы данных.
        :param users_data: Данные пользователей для создания.
        :param expected_count: Ожидаемое количество созданных пользователей.
        :raises AssertionError: Если количество пользователей или их тип не соответствует ожидаемому.
        """
        base_serv = BaseCRUDService(db_session, Users)
        for user_data in users_data:
            base_serv.create(**user_data)

        db_session.flush()

        users = base_serv.read()

        assert len(users) == expected_count
        assert all(isinstance(user, Users) for user in users)

    @pytest.mark.parametrize("users_data, filter_field, expected_count", parametrize_filter_single_field)
    def test_with_filter_single_field(self, db_session, users_data, filter_field, expected_count):
        """
        Тест проверяет корректность фильтрации записей по одному полю.

        :param users_data: Данные пользователей, передаваемые для записи в базу.
        :param filter_field: Фильтр для выборки записей.
        :param expected_count: Ожидаемое количество записей после применения фильтра.
        """
        base_serv = BaseCRUDService(db_session, Users)
        for user_data in users_data:
            base_serv.create(**user_data)

        db_session.flush()

        filters = [getattr(Users, key) == value for key, value in filter_field.items()]

        users = base_serv.read(filters=filters)
        assert len(users) == expected_count, f"Ожидалось {expected_count} записей, получено {len(users)}"

        if expected_count == 0:
            assert users == [], f"Метод read() должен вернуть пустой список, но вернул {users}"
            return

        # Проверяем, что у всех найденных пользователей значение соответствует фильтру
        key, value = next(iter(filter_field.items()))
        for user in users:
            assert getattr(user, key) == value, f"Значение {key} в {user} не совпадает с {value}"

    @pytest.mark.parametrize("users_data, filter_field, expected_count", parametrize_with_filter_multiple_fields)
    def test_with_filter_multiple_fields(self, db_session, users_data, filter_field, expected_count):
        base_serv = BaseCRUDService(db_session, Users)
        for user_data in users_data:
            base_serv.create(**user_data)

        db_session.flush()

        filters = [getattr(Users, key) == value for key, value in filter_field.items()]

        users = base_serv.read(filters=filters)
        assert len(users) == expected_count, f"Ожидалось {expected_count} записей, получено {len(users)}"

        if expected_count == 0:
            assert users == [], f"Метод read() должен вернуть пустой список, но вернул {users}"
            return

        # Проверяем, что у всех найденных пользователей значение соответствует фильтру
        for user in users:
            for key, value in filter_field.items():
                assert getattr(user, key) == value, f"Значение {key} в {user} не совпадает с {value}"

    def test_with_sorted_single_field(self, db_session):
        pass

    def test_with_sorted_any_field(self, db_session):
        pass

    def test_with_limit(self, db_session):
        pass

    def test_with_offset(self, db_session):
        pass

    def test_with_filter_sorted_limit(self, db_session):
        pass

    def test_empty_table(self):
        pass

    def test_filter_not_found(self):
        pass

    def test_read_filter_no_results(self):
        pass
