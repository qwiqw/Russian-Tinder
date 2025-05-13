from flask import Flask, render_template, request, redirect, url_for, session
import os
from data import db_session
from data.user import User
from werkzeug.security import generate_password_hash, check_password_hash

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
        form_data['link'] = request.form['link']

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
        elif not form_data['link']:
            error = 'Необходимо оставить ссылку на соц сеть'
        else:
            image = request.files['image']
            if image.filename == '':
                error = "Необходимо выбрать файл изображения."
            else:
                age = int(form_data['age'])
                count = db_sess.query(User).count()
                filename = f"image{count + 1}.jpg"
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                picture = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                user = User()
                user.name = form_data['name']
                user.gender = form_data['gender']
                user.age = age
                user.additionally = form_data['additionally']
                user.hashed_password = generate_password_hash(form_data['password'])
                user.image = picture
                user.link = form_data['link']

                db_sess.add(user)
                db_sess.commit()

                session['name'] = form_data['name']
                session['gender'] = form_data['gender']
                session['age'] = age
                session['additionally'] = form_data['additionally']
                session['image'] = picture
                session['link'] = form_data['link']

                return redirect(url_for('login'))
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
            session['link'] = user.link
            return redirect(url_for('find'))
        else:
            error = "Неверное имя пользователя или пароль."
            return redirect(url_for('find'))

    return render_template('sing_in.html', error=error)


@app.route('/find', methods=['GET', 'POST'])
def find():
    db = db_session.create_session()
    users = db.query(User).all()
    return render_template('questionnaires.html', users=users)


@app.route('/like')
def like():
    id = request.args.get('id')
    db = db_session.create_session()
    user = db.query(User).get(id)
    return render_template('like.html', link=user.link)


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(host='127.0.0.1', port=8080)
