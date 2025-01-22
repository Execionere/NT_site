import psycopg2

try:
    conn = psycopg2.connect(
        dbname='ntDB',
        user='exsi',
        password='testhome',
        host='192.168.3.2',
        port='5432'
    )
    print("Подключение успешно!")

    # Создание курсора
    cur = conn.cursor()

    # Получение списка схем
    cur.execute("SELECT schema_name FROM information_schema.schemata;")
    schemas = cur.fetchall()
    print("Доступные схемы:")
    for schema in schemas:
        print(schema[0])

    # Получение списка таблиц в конкретной схеме (например, 'public')
    test_schema = 'test_schema'  # Замените на нужную вам схему
    cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{test_schema}';")
    tables = cur.fetchall()

    print(f"\nТаблицы в схеме {test_schema}:")
    for table in tables:
        print(table[0])

except Exception as e:
    print(f"Ошибка подключения: {e}")
finally:
    # Закрытие курсора и соединения
    if cur:
        cur.close()
    if conn:
        conn.close()