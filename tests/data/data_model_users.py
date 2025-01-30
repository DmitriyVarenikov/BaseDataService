parametrize_create = [
    # Тест на создание одной записи
    ([{"nickname": "user1", "name": "Иван", "surname": "Иванов"}], 1),

    # Тест на создание нескольких записей
    ([
         {"nickname": "user1", "name": "Иван", "surname": "Иванов"},
         {"nickname": "user2", "name": "Алексей", "surname": "Петров"},
         {"nickname": "user3", "name": "Мария", "surname": "Сидорова"}
     ], 3),
]

parametrize_duplicate_name = [
    ({"nickname": "user1", "name": "Иван", "surname": "Иванов"},
     {"nickname": "user1", "name": "Иван", "surname": "Иванов"},)
]

parametrize_invalid_user_data = [
    [
        {"nickname": "", "name": "John", "surname": "Doe"},  # пустой nickname
        {"nickname": None, "name": "John", "surname": "Doe"},  # nickname = None
        {"nickname": "test", "name": None, "surname": "Doe"},  # name = None
        {"nickname": "test", "name": "", "surname": "Doe"},  # пустой name
        {"nickname": "test", "name": "John", "surname": ""},  # пустой surname
        {"nickname": "test", "name": "John", "surname": None},  # surname = None
        {}  # пустой case
    ],
]

parametrize_filter_single_field = [
    ([
         {"nickname": "user1", "name": "Иван", "surname": "Иванов"},
         {"nickname": "user2", "name": "Алексей", "surname": "Петров"},
         {"nickname": "user3", "name": "Мария", "surname": "Сидорова"}
     ], {"nickname": "user2"}, 1),

    ([
         {"nickname": "user1", "name": "Иван", "surname": "Иванов"},
         {"nickname": "user2", "name": "Алексей", "surname": "Петров"},
         {"nickname": "user3", "name": "Мария", "surname": "Сидорова"}
     ], {"name": "Мария"}, 1),

    ([
         {"nickname": "user1", "name": "Иван", "surname": "Иванов"},
         {"nickname": "user2", "name": "Алексей", "surname": "Петров"},
         {"nickname": "user3", "name": "Мария", "surname": "Сидорова"}
     ], {"surname": "Иванов"}, 1),

    ([
        {"nickname": "user1", "name": "Иван", "surname": "Иванов"},
        {"nickname": "user2", "name": "Иван", "surname": "Петров"},
        {"nickname": "user3", "name": "Иван", "surname": "Петров"}
    ], {"name": "Иван"}, 3),

    ([
         {"nickname": "user1", "name": "Иван", "surname": "Иванов"},
         {"nickname": "user2", "name": "Иван", "surname": "Петров"},
         {"nickname": "user3", "name": "Иван", "surname": "Петров"}
     ], {"name": "Empty"}, 0),

]

parametrize_with_filter_multiple_fields = [
    ([
         {"nickname": "user1", "name": "Иван", "surname": "Иванов"},
         {"nickname": "user2", "name": "Алексей", "surname": "Петров"},
         {"nickname": "user3", "name": "Мария", "surname": "Сидорова"}
     ], {"nickname": "user2", "name": "Алексей"}, 1),

    ([
         {"nickname": "user1", "name": "Иван", "surname": "Иванов"},
         {"nickname": "user2", "name": "Алексей", "surname": "Петров"},
         {"nickname": "user3", "name": "Мария", "surname": "Сидорова"}
     ], {"name": "Мария", "surname": "Empty", }, 0),

    ([
         {"nickname": "user1", "name": "Иван", "surname": "Иванов"},
         {"nickname": "user2", "name": "Алексей", "surname": "Петров"},
         {"nickname": "user3", "name": "Мария", "surname": "Сидорова"}
     ], {"name": "Мария", "surname": "Empty", }, 0),
]