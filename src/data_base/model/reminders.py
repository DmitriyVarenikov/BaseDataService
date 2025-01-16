from sqlalchemy import Column, Integer, DateTime, ForeignKey, String

from .base_model import BaseModel
from ..configuration.constrains import TableName


class Reminders(BaseModel):
    __tablename__ = TableName.REMINDERS.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(f"{TableName.USERS.value}.id"), nullable=False)
    task_description = Column(String(250), nullable=False)
    event_date = Column(DateTime, nullable=False)
    remind_before = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return (f"{TableName.REMINDERS.value}(id={self.id}, user_id={self.user_id},"
                f" task_description={self.task_description}, event_date={self.event_date},"
                f" remind_before={self.remind_before})")
