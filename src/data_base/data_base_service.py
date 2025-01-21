from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from .configuration.config import DataBaseConfig
from .model import BaseModel


class DataBaseService:
    def __init__(self, database_config: DataBaseConfig):
        self._conf = database_config
        self.engine = create_engine(self._conf.url, echo=self._conf.echo)
        self.session_local = sessionmaker(autocommit=self._conf.autocommit, autoflush=self._conf.autoflush,
                                          bind=self.engine)

    def create_tables(self) -> None:
        """Создаёт все таблицы, если их ещё нет."""
        BaseModel.metadata.create_all(self.engine)

    def drop_tables(self):
        BaseModel.metadata.drop_all(bind=self.engine)

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
