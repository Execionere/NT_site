import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, Response, render_template, jsonify
from sqlalchemy import text
import json
import uuid
import random


app = Flask(__name__)

# Настройка подключения к базе данных PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://exsi:testhome@192.168.3.2:5432/ntDB?sslmode=disable'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'test_schema.test_table'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), nullable=False)
    test_data_string = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User {self.id}, UUID: {self.uuid}, Test Data: {self.test_data_string}>'

# Пример статических данных
# users = [
#     {"id": 1, "name": "Иван", "age": 30},
#     {"id": 2, "name": "Мария", "age": 25},
#     {"id": 3, "name": "Алексей", "age": 28}
# ]

# Данные по городам
cities = [
    {"name": "Москва", "population": 11920000},
    {"name": "Якутск", "population": 300000}
]

# @app.route('/kvadrat')
# def kvadrat():
#     return render_template('kvadrat.html')

@app.route('/')
def home():
    return render_template('index.html')

def create_response(data):
    """Создает ответ в формате JSON с правильной кодировкой."""
    response_data = json.dumps(data, ensure_ascii=False)
    return Response(response_data, mimetype='application/json; charset=utf-8')

@app.route('/users', methods=['GET'])
def get_users():
    # Запрос данных из таблицы test_table
    query_get = text("SELECT id, uuid, test_data_string FROM test_schema.test_table;")
    result = db.session.execute(query_get).fetchall()

    # Преобразование результатов в список словарей
    data = [{"id": row[0], "uuid": str(row[1]), "test_data_string": row[2]} for row in result]

    # Возврат данных в формате JSON
    return create_response(data)

@app.route('/data', methods=['GET'])
def get_data():
    # Здесь можно добавить логику для возврата различных ответов
    return create_response({"message": "Это заглушка для нагрузочного тестирования!"})


@app.route('/data', methods=['POST'])
def post_data():
    data = request.json

    # Проверяем, является ли тело запроса пустым
    if data == {}:
        return create_response(cities)

@app.route('/data_add', methods=['POST'])
def data_add():
    # Генерируем новый UUID для новой записи
    new_uuid = str(uuid.uuid4())

    # Используем фиксированное значение для test_data_string
    random_number = random.randint(1, 100)
    test_data_string = (f"Тестовая строка {random_number}")  # Задаем значение напрямую

    # Создаем SQL-запрос для вставки новой записи
    insert_query = text(
        "INSERT INTO test_schema.test_table (uuid, test_data_string) VALUES (:uuid, :test_data_string);"
    )

    # Выполняем запрос с параметрами
    db.session.execute(insert_query, {'uuid': new_uuid, 'test_data_string': test_data_string})
    db.session.commit()

    return create_response({"message": "Данные успешно добавлены", "uuid": new_uuid, "string": test_data_string})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)