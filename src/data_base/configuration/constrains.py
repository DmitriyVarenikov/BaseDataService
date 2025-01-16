from enum import Enum
import os


CONFIG_FILE = os.path.join(os.getcwd(), "data_base","config.ini")


class TableName(Enum):
    USERS = "users"
    REMINDERS = "reminders"
