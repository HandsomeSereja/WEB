from flask import Flask, render_template, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(25), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    username = db.Column(db.String(30), nullable=True)
class message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=True)
    user1 = db.Column(db.String(30), nullable=True)
    user2 = db.Column(db.String(30), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/index')
def index():
    info = []
    try:
        info = Users.query.order_by(Users.id).all()
    except:
        print("ошибка чтения из БД")
    return render_template("index.html", info=info)


@app.route('/reg', methods=("POST", "GET"))
def reg():
    if request.method == "POST":
        try:
            u = Users(login=request.form['login'], username=request.form['username'], psw=request.form['psw'])
            db.session.add(u)
            db.session.flush()
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в бд")
    return render_template("reg.html")

@app.route('/user/<path>', methods=("POST", "GET"))
def user(path):
    info = []
    try:
        info = Users.query.order_by(Users.id).all()
    except:
        print("ошибка чтения из БД")
    return render_template("name.html", path=path, info=info)

@app.route('/chat/<user1>/<user2>', methods=("POST", "GET"))
def chat(user1, user2):
    info = []
    info = message.query.order_by(message.date).all()
    if request.method == "POST":
        try:
            print(request.form['text'])
            m = message(text=request.form['text'], user1=user1, user2=user2)
            db.session.add(m)
            db.session.flush()
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в бд")
    return render_template("chat.html", user1=user1, user2=user2, info=info)

@app.route('/login', methods=("POST", "GET"))
def login():
    if request.method == "POST":
        usr = []
        usr = Users.query.order_by(Users.id).all()
        try:
            log = request.form['login']
            pas = request.form['psw']
            for els in usr:
                if log == els.login:
                    if pas == els.psw:
                        print("sucess")
                        name = els.username
                        return render_template("user.html", name=name, usr=usr)
                    else:
                        print("error")
                        return "Ошибка входа"
            else:
                    print("error")
                    return "Ошибка входа"
        except:
            print("Ошибка входа")
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
