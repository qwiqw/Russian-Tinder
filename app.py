from flask import Flask, render_template, request, redirect, url_for, session
import os
import re
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/')
def landing():
    return render_template('main.html')


def is_russian(text):
    return bool(re.match(r'^[а-яА-Я\s]+$', text))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        gender = request.form['gender']
        age = int(request.form['age'])
        additionally= request.form['additionally']

        if not is_russian(name):
            error = "Имя должно содержать только русские буквы."
        elif not additionally:
            error = "Напишите что-нибудь о себе"
        elif age < 18:
            error = "Вы должны быть старше 18 лет для регистрации."
    return render_template('register.html', error=error)


@app.route('/profile')
def profile():
    if 'name' in session:
        return render_template('profile.html', user=session)
    else:
        return redirect(url_for('login'))


@app.route('/login')
def hide():
    return render_template('sing_in.html')


if __name__ == '__main__':
    db_session.global_init('db/users.db')
    app.run(host='127.0.0.1', port=8080)
