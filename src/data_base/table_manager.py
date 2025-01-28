from typing import Type, Union

from sqlalchemy.ext.declarative import DeclarativeMeta

from .model import BaseModel

class TableManager:
    def __init__(self, engine):
        self.engine = engine
        self.base_model = BaseModel

    def create_tables(self, models: Union[Type[DeclarativeMeta], list[Type[DeclarativeMeta]], None] = None) -> None:
        """Создает таблицы в базе данных для указанных моделей."""
        validation_models = self._validation_model(models)
        self._apply_to_tables(validation_models, "create")

    def drop_tables(self, models: Union[Type[DeclarativeMeta], list[Type[DeclarativeMeta]], None] = None) -> None:
        """Удаляет таблицы, если они существуют."""
        validation_models = self._validation_model(models)
        self._apply_to_tables(validation_models, "drop")

    def _validation_model(self, models: Union[Type[DeclarativeMeta], list[Type[DeclarativeMeta]], None]):
        """
        Проверяет и возвращает список моделей, которые являются подклассами базовой модели.

        :param models: Модель, список или кортеж моделей, которые необходимо проверить.
        :raises TypeError: Если передан объект некорректного типа или модель не является подклассом базовой модели.
        """
        if models is None:
            return [self.base_model]

        if isinstance(models, type):
            models = [models]

        if not isinstance(models, (list, tuple)):
            raise TypeError(f"Ожидается список или кортеж моделей, получено: {type(models)}")

        for model in models:
            if not isinstance(model, type):
                raise TypeError(f"Элемент '{model}' не является классом.")
            if not issubclass(model, self.base_model):
                raise TypeError(f"Модель '{model}' не является подклассом {self.base_model}.")

        return models

    def _apply_to_tables(self, models: Union[Type[DeclarativeMeta], list[Type[DeclarativeMeta]], None],
                         action: str) -> None:
        """Применяет указанное действие к таблицам моделей."""
        action_type = {
            "create": lambda model_obj, model_tables: model_obj.metadata.create_all(bind=self.engine,
                                                                                    tables=model_tables),
            "drop": lambda model_obj, model_tables: model_obj.metadata.drop_all(bind=self.engine, tables=model_tables),
        }

        if action not in action_type:
            raise ValueError(f"Неизвестное действие: {action}")

        for model in models:
            model_tables = None
            if hasattr(model, "__table__"):
                model_tables = [model.__table__]
            action_type[action](model, model_tables)