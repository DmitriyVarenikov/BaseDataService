from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime

from .base_model import BaseModel
from ..configuration.constrains import TableName

class Users(BaseModel):
    __tablename__ = TableName.USERS.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f"{TableName.USERS.value}(id={self.id}, nickname={self.nickname}, created_at={self.created_at}, name={self.name}, surname={self.surname})"
