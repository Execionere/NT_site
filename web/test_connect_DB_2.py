from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# Настройка подключения к базе данных PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://exsi:testhome@192.168.3.71:5432/ntDB?sslmode=disable'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def get_schemas_and_tables():
    # Получение списка всех схем
    schemas_query = text("SELECT schema_name FROM information_schema.schemata;")
    schemas = db.session.execute(schemas_query).fetchall()

    print("Доступные схемы:")
    for schema in schemas:
        schema_name = schema[0]
        # Игнорируем схему public
        if schema_name == 'test_schema':
            print(schema_name)

        tables_query = text(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}';")
        tables = db.session.execute(tables_query).fetchall()

        print(f"Таблицы в схеме {schema_name}:")
        for table in tables:
            print(f" - {table[0]}")

            # Запрос данных из таблицы test_table
            if table[0] == 'test_table':
                data_query = text(f"SELECT * FROM {schema_name}.{table[0]};")
                data_rows = db.session.execute(data_query).fetchall()

                print(f"\nДанные в таблице {table[0]}:")
                for row in data_rows:
                    print(row)

        # Запрос данных из таблицы test_table
        query = text("SELECT id, uuid, test_data_string FROM test_schema.test_table;")
        result = db.session.execute(query).fetchall()

        # Преобразование результатов в список словарей
        data = [{"id": row[0], "uuid": str(row[1]), "test_data_string": row[2]} for row in result]

        # Возврат данных в формате JSON
        return jsonify(data)


if __name__ == '__main__':
    with app.app_context():
        get_schemas_and_tables()
