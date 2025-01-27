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
        {} # пустой case
    ],
]
