from contextlib import nullcontext

import pytest

from src.data_base.model import Users, Reminders


parametrize_create_tables_with_specific_models = [
    (Users, "users", nullcontext()),
    (Reminders, "reminders", nullcontext()),
    ([Users, Reminders], ["users", "reminders"], nullcontext()),
    (None, ["users", "reminders"], nullcontext()),
    ("...", ["users", "reminders"], pytest.raises(TypeError))
]
