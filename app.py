from flask import Flask, render_template, request, redirect, url_for, session
import os
import re
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


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

            session['name'] = name
            session['password'] = hashed_password
            session['gender'] = gender
            session['age'] = age
            session['education'] = education
            session['profession'] = profession

            return redirect(url_for('profile'))

    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if 'name' in session and session['name'] == name and session['password'] == hashed_password:
            return redirect(url_for('profile'))
        else:
            error = "Неверное имя пользователя или пароль"

    return render_template('sing_in.html', error=error)


@app.route('/profile')
def profile():
    if 'name' in session:
        return render_template('profile.html', user=session)
    else:
        return redirect(url_for('sing_in'))


if __name__ == '__main__':
    app.run(debug=True)
