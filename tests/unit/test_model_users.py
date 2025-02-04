from dataclasses import field

import pytest

from sqlalchemy import text, asc, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.testing.suite import PrecisionIntervalTest

from src.data_base.model import Users
from src.data_base.service_model.base_service import BaseCRUDService
from ..data.data_model_users import parametrize_create, parametrize_duplicate_name, parametrize_invalid_user_data, \
    parametrize_filter_single_field, parametrize_with_filter_multiple_fields, parametrize_with_sorted_single_field, \
    parametrize_sorting_by_multiple_fields, parametrize_create_valid, parametrize_with_filter_sorted_limit


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
#  Чтение записей, когда в таблице нет данных. +
#  Чтение записей по одному полю (фильтрация). +
#  Чтение записей по нескольким полям (сложная фильтрация). +
#  Чтение записей, когда фильтр не соответствует ни одной записи. +
#  Чтение записей с сортировкой по одному полю. +
#  Чтение записей с сортировкой по нескольким полям. +
#  Чтение записей с лимитом (ограничение количества). +
#  Чтение записей с оффсетом. +
#  Чтение записей с комбинацией фильтрации, сортировки и лимита. +


def _create_users(db_session, users_data):
    base_serv = BaseCRUDService(db_session, Users)
    for user_data in users_data:
        base_serv.create(**user_data)
    db_session.flush()
    return base_serv


@pytest.mark.usefixtures("setup_users_table")
class TestUsersCRUDRead:

    @pytest.mark.parametrize("users_data, expected_count", parametrize_create)
    def test_all(self, db_session, users_data, expected_count):
        """
        Тестирует создание пользователей и проверяет общее количество созданных записей, а также корректность данных.

        :param db_session: Текущая сессия базы данных для выполнения операций.
        :param users_data: Данные пользователей, используемые для тестирования.
        :param expected_count: Ожидаемое количество созданных пользователей.
        """
        base_serv = _create_users(db_session, users_data)

        users = base_serv.read()

        assert len(users) == expected_count

        for user_data, user in zip(users_data, users):
            actual_data = {field: getattr(user, field) for field in user_data}
            assert user_data == actual_data

    @pytest.mark.parametrize("users_data, filter_field, expected_count", parametrize_filter_single_field)
    def test_with_filter_single_field(self, db_session, users_data, filter_field, expected_count):
        """
        Тест проверяет корректность фильтрации записей по одному полю.

        :param users_data: Данные пользователей, передаваемые для записи в базу.
        :param filter_field: Фильтр для выборки записей.
        :param expected_count: Ожидаемое количество записей после применения фильтра.
        """
        base_serv = _create_users(db_session, users_data)

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
        base_serv = _create_users(db_session, users_data)

        filters = [getattr(Users, key) == value for key, value in filter_field.items() if hasattr(Users, key)]
        users = list() if not filters else base_serv.read(filters=filters)

        assert len(users) == expected_count, f"Ожидалось {expected_count} записей, получено {len(users)}"

        if expected_count == 0:
            assert users == [], f"Метод read() должен вернуть пустой список, но вернул {users}"
            return

        # Проверяем, что у всех найденных пользователей значение соответствует фильтру
        for user in users:
            for key, value in filter_field.items():
                assert getattr(user, key) == value, f"Значение {key} в {user} не совпадает с {value}"

    @pytest.mark.parametrize("users_data,  expected_order", parametrize_with_sorted_single_field)
    def test_with_sorted_single_field(self, db_session, users_data, expected_order):
        """
        Тестирует сортировку записей пользователей по отдельным полям в порядке возрастания и убывания.

        :param db_session: Сессия базы данных для выполнения операций.
        :param users_data: Данные пользователей для создания записей в базе данных.
        :param expected_order: Ожидаемый порядок пользователей после сортировки.
        """
        base_serv = _create_users(db_session, users_data)

        # Сортировка по полю  nickname (ASC/DESC)
        print(type(Users.nickname), 11111)
        users = base_serv.read(order_by=Users.nickname)
        assert [user.nickname for user in users] == list(expected_order)
        users = base_serv.read(order_by=Users.nickname.desc())
        assert [user.nickname for user in users] == list(expected_order)[::-1]

        # Сортировка по полю  name (ASC/DESC)
        users = base_serv.read(order_by=Users.name)
        assert [user.name for user in users] == list(expected_order)
        users = base_serv.read(order_by=Users.name.desc())
        assert [user.name for user in users] == list(expected_order)[::-1]

        # Сортировка по полю  surname (ASC/DESC)
        users = base_serv.read(order_by=Users.surname)
        assert [user.surname for user in users] == list(expected_order)
        users = base_serv.read(order_by=Users.surname.desc())
        assert [user.surname for user in users] == list(expected_order)[::-1]

    @pytest.mark.parametrize("users_data, sorting_rules", parametrize_sorting_by_multiple_fields)
    def test_sorting_by_multiple_fields(self, db_session, users_data, sorting_rules):
        base_serv = _create_users(db_session, users_data)

        for sort_direction, field_combinations in sorting_rules.items():
            for fields in field_combinations:
                try:
                    order_by = [(asc if sort_direction == "asc" else desc)(getattr(Users, field)) for field in fields]
                except AttributeError as ex:
                    pytest.fail(f"Ошибка доступа к полю {ex}")

                expected_users = db_session.query(Users).order_by(*order_by).all()
                users = base_serv.read(order_by=order_by)

                assert [
                           tuple(getattr(user, field) for field in fields) for user in expected_users
                       ] == [
                           tuple(getattr(user, field) for field in fields) for user in users
                       ], f"Ошибка при сортировке по {fields} в порядке {sort_direction}"

    @pytest.mark.parametrize("users_data", parametrize_create_valid)
    def test_with_limit(self, db_session, users_data):
        base_serv = _create_users(db_session, users_data)
        max_limit = len(users_data)
        for limit in range(1, max_limit):
            expected_users = db_session.query(Users).limit(limit).all()
            users = base_serv.read(order_by=Users.id, limit=limit)
            assert len(expected_users) == len(users)
            assert [expected_users.id for expected_users in users] == [user.id for user in users]

    @pytest.mark.parametrize("users_data", parametrize_create_valid)
    def test_with_offset(self, db_session, users_data):
        base_serv = _create_users(db_session, users_data)
        total_count = db_session.query(Users).count()
        for offset in range(total_count + 1):
            expected_users = db_session.query(Users).order_by(Users.id).offset(offset).all()
            users = base_serv.read(order_by=Users.id, offset=offset)
            assert len(expected_users) == len(users)
            assert [user.id for user in expected_users] == [user.id for user in users]

    @pytest.mark.parametrize("users_data, test_cases", parametrize_with_filter_sorted_limit)
    def test_with_filter_sorted_limit(self, db_session, users_data, test_cases):
        base_serve = _create_users(db_session, users_data)
        for test_case in test_cases:
            query_params, expected_users = test_case
            users = base_serve.read(
                filters=[getattr(Users, field) == value for field, value in query_params["filter"].items()],
                order_by=query_params["order_by"],
                limit=query_params["limit"])

            assert len(users) == len(expected_users)
            for user, expected_user in zip(users, expected_users):
                assert user.nickname == expected_user["nickname"]
                assert user.name == expected_user["name"]
                assert user.surname == expected_user["surname"]