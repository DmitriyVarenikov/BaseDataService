from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, Optional, Any, Union
from sqlalchemy.sql.expression import BinaryExpression
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

    def update(self, filters: list[Any], updates: dict, use_or: bool = False, ) -> int:
        """
        Обновляет записи в базе данных на основе заданных условий и значений для обновления.

        :param filters: Список условий фильтрации SQLAlchemy.
        :param updates: Словарь с данными для обновления.
        :param use_or: Если True, применяет логическое "или" к фильтрам; иначе применяет "и". По умолчанию False.
        :raises TypeError: Если filters не является списком, updates не является словарём или filters содержит элементы, не являющиеся SQLAlchemy условиями фильтрации.
        :raises ValueError: Если filters пуст или updates не содержит данных.
        """
        if not isinstance(filters, list):
            raise TypeError(f"filters должен быть списком, а не {type(filters).__name__}")

        if not filters:
            raise ValueError("Не переданы условия фильтрации")

        if not all(isinstance(f, BinaryExpression) for f in filters):
            raise TypeError("filters должен содержать только условия фильтрации SQLAlchemy")

        if not isinstance(updates, dict):
            raise TypeError(f"updates должен быть словарём, а не {type(updates).__name__}")

        if not updates:
            raise ValueError("Не переданы данные для обновления")

        query = self._session.query(self._model)
        query = query.filter(or_(*filters) if use_or else and_(*filters))
        updated_count = query.update(updates, synchronize_session="fetch")
        return updated_count

    def read(self,
             filters: Optional[list[BinaryExpression]] = None,
             use_or: bool = False,
             order_by = None,
             limit: int = None,
             offset: int = None) -> list[T]:
        """
        Читает данные из базы данных с использованием заданных фильтров, сортировки, лимита и смещения.

        :param filters: Список условий фильтрации SQLAlchemy, опционально.
        :param use_or: Определяет, использовать ли логическое "ИЛИ" вместо "И" при применении фильтров. По умолчанию False.
        :param order_by: Порядок сортировки. Может быть одиночным условием или списком условий.
        :param limit: Максимальное количество возвращаемых записей. Опционально.
        :param offset: Смещение записей. Опционально.
        :raises TypeError: Если переданные фильтры не являются списком или содержат некорректные условия.
        """
        query = self._session.query(self._model)

        if filters:
            if not isinstance(filters, list):
                raise TypeError(f"filters должен быть списком, а не {type(filters).__name__}")

            if not all(isinstance(f, BinaryExpression) for f in filters):
                raise TypeError("filters должен содержать только условия фильтрации SQLAlchemy")

            query = query.filter(or_(*filters) if use_or else and_(*filters))

        if order_by is not None:
            if isinstance(order_by, list):
                query = query.order_by(*order_by)
            else:
                query = query.order_by(order_by)

        if limit is not None:
            query = query.limit(limit)

        if offset is not None:
            query = query.offset(offset)

        return query.all()
