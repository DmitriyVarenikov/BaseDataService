from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, Optional, Any

from src.data_base.model.base_model import BaseModel
from sqlalchemy import and_, or_

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

    def read(self,
             filters: Optional[list[Any]] = None,
             use_or: bool = False,
             order_by=None,
             limit: int = None,
             offset: int = None) -> list[T]:
        """
        Читает данные из базы данных на основе заданных фильтров и параметров сортировки.

        :param filters: Список фильтров для применения к запросу.
        :param use_or: Логическое значение, определяющее использование логического "ИЛИ" вместо "И" для фильтров.
        :param order_by: Поле или список полей для сортировки результатов.
        :param limit: Максимальное количество возвращаемых записей.
        :param offset: Смещение количества пропускаемых записей от начала.
        """
        query = self._session.query(self._model)

        if filters:
            query = query.filter(or_(*filters) if use_or else and_(*filters))

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
