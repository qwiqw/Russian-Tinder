from flask import Flask, render_template, request, redirect, url_for, session
import os
import re
from data import db_session
from data.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/')
def landing():
    return render_template('main.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    oshibochka = None
    formochka_dannih = {}

    if request.method == 'POST':
        formochka_dannih['name'] = request.form['name']
        formochka_dannih['password'] = request.form['password']
        formochka_dannih['gender'] = request.form['gender']
        formochka_dannih['age'] = request.form['age']
        formochka_dannih['additionally'] = request.form['additionally']

        db_sess = db_session.create_session()
        existing_user = db_sess.query(User).filter(User.name == formochka_dannih['name']).first()

        if existing_user:
            oshibochka = "Пользователь с таким именем уже зарегистрирован."
        elif not formochka_dannih['additionally']:
            oshibochka = "Напишите что-нибудь о себе"
        elif not formochka_dannih['age'].isdigit() or int(formochka_dannih['age']) < 18:
            oshibochka = "Вы должны быть старше 18 лет для регистрации."
        elif 'image' not in request.files:
            oshibochka = "Необходимо загрузить изображение профиля."
        else:
            image = request.files['image']
            if image.filename == '':
                oshibochka = "Необходимо выбрать файл изображения."
            else:
                age = int(formochka_dannih['age'])
                imya_faila = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], imya_faila))
                izobrajenie = os.path.join(app.config['UPLOAD_FOLDER'], imya_faila)

                polzovatel = User()
                polzovatel.name = formochka_dannih['name']
                polzovatel.gender = formochka_dannih['gender']
                polzovatel.age = age
                polzovatel.additionally = formochka_dannih['additionally']
                polzovatel.hashed_password = generate_password_hash(formochka_dannih['password'])
                polzovatel.image = izobrajenie

                db_sess.add(polzovatel)
                db_sess.commit()

                session['name'] = formochka_dannih['name']
                session['gender'] = formochka_dannih['gender']
                session['age'] = age
                session['additionally'] = formochka_dannih['additionally']
                session['image'] = izobrajenie

                return redirect(url_for('profile'))
    else:
        formochka_dannih = {}
    return render_template('register.html', error=oshibochka, form_data=formochka_dannih)


@app.route('/profile')
def profile():
    if 'name' in session:
        return render_template('profile.html', user=session)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == name).first()

        if user and check_password_hash(user.hashed_password, password):
            session['name'] = user.name
            session['gender'] = user.gender
            session['age'] = user.age
            session['additionally'] = user.additionally
            session['image'] = user.image
            return redirect(url_for('profile'))
        else:
            error = "Неверное имя пользователя или пароль."

    return render_template('sing_in.html', error=error)


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(host='127.0.0.1', port=8080)
