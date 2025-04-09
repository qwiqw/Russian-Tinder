from flask import Flask, render_template
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'russian-tinder-secret-key'


@app.route('/')
def astronaut_selection():
    return render_template('main.html')


def main():
    app.run()


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    main()
