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
    error = None
    form_data = {}

    if request.method == 'POST':
        form_data['name'] = request.form['name']
        form_data['password'] = request.form['password']
        form_data['gender'] = request.form['gender']
        form_data['age'] = request.form['age']
        form_data['additionally'] = request.form['additionally']

        db_sess = db_session.create_session()
        existing_user = db_sess.query(User).filter(User.name == form_data['name']).first()

        if existing_user:
            error = "Пользователь с таким именем уже зарегистрирован."
        elif not form_data['additionally']:
            error = "Напишите что-нибудь о себе"
        elif not form_data['age'].isdigit() or int(form_data['age']) < 18:
            error = "Вы должны быть старше 18 лет для регистрации."
        elif 'image' not in request.files:
            error = "Необходимо загрузить изображение профиля."
        else:
            image = request.files['image']
            if image.filename == '':
                error = "Необходимо выбрать файл изображения."
            else:
                age = int(form_data['age'])
                name_surname = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], name_surname))
                picture = os.path.join(app.config['UPLOAD_FOLDER'], name_surname)

                user = User()
                user.name = form_data['name']
                user.gender = form_data['gender']
                user.age = age
                user.additionally = form_data['additionally']
                user.hashed_password = generate_password_hash(form_data['password'])
                user.image = picture

                db_sess.add(user)
                db_sess.commit()

                session['name'] = form_data['name']
                session['gender'] = form_data['gender']
                session['age'] = age
                session['additionally'] = form_data['additionally']
                session['image'] = picture

                return redirect(url_for('profile'))
    else:
        form_data = {}
    return render_template('register.html', error=error, form_data=form_data)


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

@app.route('/find', methods=['GET', 'POST'])
def find():
    pass


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(host='127.0.0.1', port=8080)
