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

    ([
         {"nickname": "user1", "name": "Алексей", "surname": "Иванов"},
         {"nickname": "user2", "name": "Алексей", "surname": "Петров"},
         {"nickname": "user3", "name": "Мария", "surname": "Сидорова"}
     ], {"name": "Алексей"}, 2),

    ([
         {"nickname": "user1", "name": "Иван", "surname": "Иванов"},
         {"nickname": "user2", "name": "Алексей", "surname": "Петров"},
         {"nickname": "user3", "name": "Мария", "surname": "Сидорова"}
     ], {"age": 30}, 0),
]

parametrize_with_sorted_single_field = [
    ([
         {"nickname": "B", "name": "A", "surname": "C"},
         {"nickname": "A", "name": "C", "surname": "A"},
         {"nickname": "C", "name": "B", "surname": "B"}
     ], ("A", "B", "C")),
]

parametrize_sorting_by_multiple_fields = [
    ([
         {"id": 2, "nickname": "B", "name": "A", "surname": "C"},
         {"id": 1, "nickname": "A", "name": "C", "surname": "A"},
         {"id": 3, "nickname": "C", "name": "B", "surname": "B"},
         {"id": 4, "nickname": "D", "name": "A", "surname": "B"}
     ],

     {
         "asc": [("nickname", "name"), ("nickname", "name", "surname"), ("id", "surname", "name")],
         "desc": [("nickname", "name"), ("nickname", "name", "surname"), ("id", "surname", "name")],
     }
    )
]

parametrize_create_valid = [
    ([
        {"nickname": "B", "name": "A", "surname": "C"},
        {"nickname": "A", "name": "C", "surname": "A"},
        {"nickname": "C", "name": "B", "surname": "B"},
        {"nickname": "D", "name": "A", "surname": "B"}
    ]
    )
]

parametrize_with_filter_sorted_limit = [
    (
        # Данные пользователей
        [
            {"nickname": "B", "name": "A", "surname": "C"},
            {"nickname": "A", "name": "C", "surname": "A"},
            {"nickname": "C", "name": "B", "surname": "B"},
            {"nickname": "D", "name": "A", "surname": "B"}
        ],
        # Тестовые случаи
        [
            (
                {"filter": {"nickname": "A"}, "order_by": "name", "limit": 1},
                [{"nickname": "A", "name": "C", "surname": "A"}]
            ),
            (
                {"filter": {"name": "A"}, "order_by": "surname", "limit": 2},
                [{"nickname": "D", "name": "A", "surname": "B"},
                 {"nickname": "B", "name": "A", "surname": "C"}]
            ),
            (
                {"filter": {"surname": "B"}, "order_by": "nickname", "limit": 10},
                [{"nickname": "C", "name": "B", "surname": "B"},
                 {"nickname": "D", "name": "A", "surname": "B"}]
            ),
            (
                {"filter": {"nickname": "Z"}, "order_by": "name", "limit": 5},  # Фильтр не найдёт ничего
                []
            ),
        ]
    )
]

