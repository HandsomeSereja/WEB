from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(25), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    username = db.Column(db.String(30), nullable=True)


class message(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=True)
    user1 = db.Column(db.String(30), nullable=True)
    user2 = db.Column(db.String(30), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    serialize_only = ('text', 'user1', 'user2')


@app.route('/index', methods=("POST", "GET"))
def index():
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
                        return render_template("user.html", name=name)
                    else:
                        print("error")
                        flash('Ошибка авторизации')
            else:
                    print("error")
                    flash('Ошибка авторизации')
        except:
            print("Ошибка входа")
    return render_template("index.html")


@app.route('/reg', methods=("POST", "GET"))
def reg():
    if request.method == "POST":
        try:
            u = Users(login=request.form['login'], username=request.form['username'], psw=request.form['psw'])
            db.session.add(u)
            db.session.flush()
            db.session.commit()
            return render_template("index.html")
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
    if request.method == "POST":
        try:
            u = message(text=request.json['text'], user1=request.json['user1'], user2=request.json['user2'])
            db.session.add(u)
            db.session.flush()
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в бд")
    if request.method == "GET":
        try:
            print("отправка")
            info = []
            info = message.query.order_by(message.date).all()
            print(info.to_dict)
        except:
            print("ошибка отправки")
    return render_template("chat.html", user1=user1, user2=user2)

@app.route('/api')
def api():
    data = []
    for u in message.query.all():
        data.append(u.text)
    print(data)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
