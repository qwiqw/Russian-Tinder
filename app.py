from flask import Flask, render_template, request, redirect, url_for, session
import os
import re
import hashlib
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

DATABASE = 'db/users.db'


def create_db():
    """Создает базу данных, если она не существует, и таблицу users."""
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            gender TEXT NOT NULL,
            age INTEGER NOT NULL,
            education TEXT NOT NULL,
            profession TEXT NOT NULL
        )
    ''')
    db.commit()
    db.close()


def get_db():
    """Подключается к базе данных."""
    db = sqlite3.connect(DATABASE)
    return db


@app.route('/')
def landing():
    return render_template('main.html')


def is_russian(text):
    """Проверяет, состоит ли строка только из русских букв и пробелов."""
    return bool(re.match(r'^[а-яА-Я\s]+$', text))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        gender = request.form['gender']
        age = int(request.form['age'])
        education = request.form['education']
        profession = request.form['profession']

        if not is_russian(name):
            error = "Имя должно содержать только русские буквы."
        elif not is_russian(profession):
            error = "Профессия должна быть на русском языке."
        elif not is_russian(education):
            error = "Образование должно быть на русском языке."
        elif age < 18:
            error = "Вы должны быть старше 18 лет для регистрации."
        else:
            name = name.capitalize()
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            db = get_db()
            cursor = db.cursor()
            try:
                cursor.execute('''
                    INSERT INTO users (name, password, gender, age, education, profession)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, hashed_password, gender, age, education, profession))
                db.commit()
                session['name'] = name
                session['password'] = hashed_password
                session['gender'] = gender
                session['age'] = age
                session['education'] = education
                session['profession'] = profession
                db.close()  # Close db before redirect
                return redirect(url_for('profile'))

            except sqlite3.Error as e:
                error = f"Ошибка базы данных: {e}"
                db.close() # Close the database even on error
                return render_template('register.html', error=error) # Return the form with the error

            finally:  # This is no longer needed, since DB is closed in each branch.
                pass


    return render_template('register.html', error=error) # Return form on GET requests


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE name = ? AND password = ?', (name, hashed_password))
        user = cursor.fetchone()
        db.close()

        if user:
            session['name'] = user[1]  # Предполагается, что имя находится во втором столбце
            session['password'] = user[2]
            session['gender'] = user[3]
            session['age'] = user[4]
            session['education'] = user[5]
            session['profession'] = user[6]

            return redirect(url_for('profile'))
        else:
            error = "Неверное имя пользователя или пароль"

    return render_template('sing_in.html', error=error)

@app.route('/profile')
def profile():
    if 'name' in session:
        return render_template('profile.html', user=session)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    # Create the 'db' directory if it doesn't exist
    if not os.path.exists('db'):
        os.makedirs('db')
    create_db()  # Create the database if it doesn't exist

    app.run(debug=True)
