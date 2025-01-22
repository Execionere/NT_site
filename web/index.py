from flask import render_template
from em02_web import app  # Импортируем экземпляр приложения

@app.route('/home')
def home():
    return render_template('index.html')