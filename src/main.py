from src.data_base.data_base_service import DataBaseService
from src.data_base.types_db import DataBaseType
from src.data_base.service_model.base_service import BaseCRUDService
from src.data_base.model import Users

if __name__ == "__main__":
    data_user = data = {"nickname": "john_doe", "name": "John", "surname": "Doe"}
    db = DataBaseService(DataBaseType.SQLite)
    db.create_tables()
    # with db.session_scope() as session:
    #     ms = BaseCRUDService(session, Users)
    #     ms.create(**data_user)