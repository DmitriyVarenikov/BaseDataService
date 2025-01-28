from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from .configuration import DataBaseConfig


class DataBaseService:
    """
    Класс DataBaseService предоставляет методы для работы с базой данных, включая создание таблиц,
     удаление таблиц и управление сессиями.
    """

    def __init__(self, database_config: DataBaseConfig, engine):
        try:
            self.engine = engine
            self.conf = database_config
            self.session_local = sessionmaker(autocommit=self.conf.autocommit, autoflush=self.conf.autoflush,
                                              bind=self.engine)
        except Exception as ex:
            raise RuntimeError(f"Не удалось инициализировать DataBaseService: {ex}")

    @contextmanager
    def session_scope(self, commit=True):
        """
        Предоставляет контекстный менеджер для управления сессией базы данных.

        :param commit: Указывает, следует ли выполнять commit изменений в сессии. По умолчанию True.
        :raises Exception: Выбрасывается в случае ошибки выполнения в сессии, с последующим откатом изменений.
        """
        session = self.session_local()
        try:
            yield session
            if commit:
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Session rollback due to: {e}")
            raise
        finally:
            session.close()
