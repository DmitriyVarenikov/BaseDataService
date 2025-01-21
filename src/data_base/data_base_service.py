from contextlib import contextmanager
from typing import Type, Union

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .configuration.config import DataBaseConfig
from .model import BaseModel


class DataBaseService:
    def __init__(self, database_config: DataBaseConfig):
        try:
            self.conf = database_config
            self.engine = create_engine(self.conf.url, echo=self.conf.echo)
            self.session_local = sessionmaker(autocommit=self.conf.autocommit, autoflush=self.conf.autoflush,
                                              bind=self.engine)
            self.base_model = BaseModel
        except Exception as ex:
            raise RuntimeError(f"Не удалось инициализировать DataBaseService: {ex}")

    def create_tables(self, models: Union[Type[DeclarativeMeta], list[Type[DeclarativeMeta]], None] = None) -> None:
        """Создаёт все таблицы, если их ещё нет."""
        self._apply_to_tables(models, "create")

    def drop_tables(self, models: Union[Type[DeclarativeMeta], list[Type[DeclarativeMeta]], None] = None) -> None:
        """Удаляет таблицы. Если модели не переданы, удаляет все таблицы."""
        self._apply_to_tables(models, "drop")

    def _apply_to_tables(self, models: Union[Type[DeclarativeMeta], list[Type[DeclarativeMeta]], None], action: str) -> None:
        action_type = {
            "create": lambda model_obj, model_tables: model_obj.metadata.create_all(bind=self.engine, tables=model_tables),
            "drop": lambda model_obj, model_tables: model_obj.metadata.drop_all(bind=self.engine, tables=model_tables),
        }


        if action not in action_type:
            raise ValueError(f"Неизвестное действие: {action}")

        models = [self.base_model] if models is None else ([models] if isinstance(models, type) else models)

        for model in models:
            model_tables = None
            if not isinstance(model, type) or not issubclass(model, self.base_model):
                raise TypeError(f"Неверный тип модели: {model}")
            if hasattr(model, "__table__"):
                model_tables = [model.__table__]
            action_type[action](model, model_tables)

    @contextmanager
    def session_scope(self):
        """контекстный менеджер сессии"""
        session = self.session_local()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Session rollback due to: {e}")
            raise
        finally:
            session.close()
