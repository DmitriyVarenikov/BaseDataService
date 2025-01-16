from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic

from src.data_base.model.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseCRUDService(Generic[T]):
    """Базовый класс для реализации CRUD (Create, Read, Update, Delete) операций."""

    def __init__(self, session: Session, model: Type[T]):
        """
        :param session: Сессия SQLAlchemy.
        :param model: Класс модели базы данных.
        """
        self._session = session
        self._model = model

    def create(self, **kwargs) -> T:
        """
        Создание новой записи в базе данных.

        :param kwargs: Данные для создания новой записи. Имя поля: значение.
        :return: Созданный объект модели.
        """
        instance = self._model(**kwargs)
        self._session.add(instance)
        return instance

    def delete(self, **filters) -> int:
        """
        Удаление записей из базы данных на основе фильтров.

        :param filters: Условия фильтрации для удаления записей.  Ключи — имена полей, значения — условия фильтрации.
        :return: Количество удалённых записей.
        """
        query = self._session.query(self._model).filter_by(**filters)
        deleted_count = query.delete(synchronize_session="fetch")
        return deleted_count

    def update(self, filters: dict, updates: dict) -> int:
        """
        Обновляет записи, соответствующие фильтрам, новыми значениями.

        :param filters: Словарь с условиями для выбора записей.
        :param updates: Словарь с полями и их новыми значениями.
        :return: Количество обновлённых записей.
        """
        if not updates:
            raise ValueError("")

        query = self._session.query(self._model).filter_by(**filters)
        updated_count = query.update(updates, synchronize_session="fetch")
        return updated_count

    def read(self, filters: dict = None, order_by=None, limit: int = None, offset: int = None) -> list[T]:
        """
        Чтение записей из базы данных на основе фильтров и параметров.

        :param filters: Словарь с условиями для фильтрации записей (опционально).
        :param order_by: Поле или список полей для сортировки (опционально).
        :param limit: Ограничение на количество возвращаемых записей (опционально).
        :param offset: Смещение для пагинации (опционально).
        :return: Список объектов модели.
        """

        query = self._session.query(self._model)

        if filters:
            query = query.filter_by(**filters)

        if order_by:
            if isinstance(order_by, list):
                query = query.order_by(*order_by)
            else:
                query = query.order_by(order_by)

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        return query.all()


from sqlalchemy.orm import Session
from sqlalchemy_mixins import AllFeaturesMixin

class BaseService(AllFeaturesMixin):
    """
    Класс для базового CRUD-сервиса, использующий sqlalchemy_mixins.
    """
    def __init__(self, session: Session):
        """
        Инициализация сервиса с сессией.
        :param session: Экземпляр SQLAlchemy Session.
        """
        if not session:
            raise ValueError("Session cannot be None")
        self.set_session(session)

    def create(self, **kwargs):
        """
        Создание новой записи.
        :param kwargs: Данные для новой записи.
        :return: Созданная запись.
        """
        instance = self.create_instance(**kwargs)
        self.session.commit()
        return instance

    def update(self, filters: dict, updates: dict):
        """
        Обновление записей по фильтрам.
        :param filters: Условия фильтрации записей.
        :param updates: Новые данные для обновления.
        :return: Количество обновленных записей.
        """
        if not updates:
            raise ValueError("No updates provided for the update operation")
        count = self.filter_by(**filters).update(updates, synchronize_session="fetch")
        self.session.commit()
        return count

    def delete(self, **filters):
        """
        Удаление записей по фильтрам.
        :param filters: Условия фильтрации записей.
        :return: Количество удаленных записей.
        """
        count = self.filter_by(**filters).delete(synchronize_session="fetch")
        self.session.commit()
        return count

    def read(self, filters: dict = None, order_by=None, limit=None, offset=None):
        """
        Чтение записей с фильтрами и сортировкой.
        :param filters: Условия фильтрации записей.
        :param order_by: Поле для сортировки.
        :param limit: Лимит записей.
        :param offset: Смещение записей.
        :return: Список найденных записей.
        """
        query = self.filter_by(**filters) if filters else self.query

        if order_by:
            query = query.order_by(*order_by) if isinstance(order_by, list) else query.order_by(order_by)

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        return query.all()
