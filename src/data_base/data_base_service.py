from sndhdr import tests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from .configuration.config import DataBaseConfig
from .model import BaseModel

class DataBaseService:
    def __init__(self, database_config: DataBaseConfig):
        self.conf = database_config
        self.engine = create_engine(self.conf.url, echo=True)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        """Создает новую сессию для работы с базой данных."""
        return self.session_local()

    def create_tables(self) -> None:
        """Создаёт все таблицы, если их ещё нет."""
        BaseModel.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self):
        """контекстный менеджер сессии"""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Session rollback due to: {e}")
            raise
        finally:
            session.close()



# project
#     |_ src
#     |   |_ data_base
#     |   |    |_ configuration
#     |   |    |    |_ config.py
#     |   |    |    |_ constrains.py
#     |   |    |
#     |   |    |_ model
#     |   |    |   |_ base_model.py
#     |   |    |   |_ reminders.py
#     |   |    |   |_ users.py
#     |   |    |
#     |   |    |_ service_model
#     |   |    |   |_ base_service
#     |   |    |
#     |   |    |_ config.ini
#     |   |    |_ config_loader.py
#     |   |    |_ data_base_service.py
#     |   |    |_types_db.py
#     |   |
#     |   |
#     |   |_ main.py
#     |
#     |_ tests
#         |_ test_data_base_service.py