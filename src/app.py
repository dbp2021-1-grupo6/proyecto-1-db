import json

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import ValidationError

app = Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/proyecto1dbp'
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.secret_key = b'_5#y2L"F4Qpz\n\xec]/'


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    balance = db.Column(db.Float(precision=2), nullable=False)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    image_url = db.Column(db.String(256), nullable=False)


class Inventory(db.Model):
    g_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    c_id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True)


db.create_all()


@app.route('/')
def redirect_home():
    return redirect(url_for('home'))


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html', res=None)


@app.route('/games', methods=['GET', 'POST'])
def print_tiendas():
    if request.method == 'GET':
        res = None
        return render_template('game.html', res = res,  data=Game.query.all())
    else:
        content = json.loads(request.data)
        login_id = 3
        print(content['id'])
        if Inventory.query.filter_by(c_id=login_id, g_id=content['id']).first() is not None:
            raise ValidationError('Juego ya comprado')
        elif Client.query.filter_by(id=login_id).first().balance < Game.query.filter_by(id=content['id']).first().price:
            raise ValidationError('Fondos Insuficientes')
        else:
            client = Client.query.filter_by(id=login_id).first()
            client.balance -= Game.query.filter_by(id=content['id']).first().price
            db.session.add(Inventory(g_id=content['id'], c_id=login_id))
            db.session.commit()
            return json.dumps({'message': "ok"})


@app.route('/inventory/<user_id>', methods=['GET', 'DELETE'])
def print_stock(user_id):
    if request.method == 'GET':
        return render_template('inventory.html', data=db.session.query(Game)
                               .join(Inventory)
                               .filter(Game.id == Inventory.g_id, Inventory.c_id == user_id).all())
    else:
        content = json.loads(request.data)
        login_id = 3
        print(content['id'])
        Inventory.query.filter_by(c_id=login_id, g_id=content['id']).delete()
        db.session.commit()
        return json.dumps({'message': "ok"})


@app.route('/register', methods=['GET', 'POST'])
def register_user_get():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        content = request.form
        user = content['username']
        passw = content['psw']
        passw_confirm = content['psw-repeat']
        if passw != passw_confirm:
            flash("Las contraseñas no coinciden")
            return redirect(url_for('register_user_get'))
        elif len(user) > 32 or len(passw) > 32:
            flash("Pruebe con un Username/Password mas corto")
            return redirect(url_for('register_user_get'))
        elif Client.query.filter_by(username=user).first() is not None:
            flash("Ya existe un usuario con ese Username")
            return redirect(url_for('register_user_get'))
        db.session.add(Client(username=content['username'], password=content['psw'], balance=200))
        db.session.commit()
        db.session.close()
        return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    res = {
        'username': '',
        'estado': 0, # si es cero hay error en logeo, si es 1 todo correcto,
        'mensaje': ''
    }


    if(request.method == 'POST'): 
        # content = json.loads(request.data)
        content = request.form
        client = Client.query.filter_by(username=content['username']).first()
        if client is not None:
            if client.password == content['psw']:
                res = {'username': content['username']}
                return render_template('home.html', res=res)
            else:
                flash("Contraseña Incorrecta")
                return redirect(url_for('login'))
        else:
            flash("Usuario no existente")
            return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/profile', methods=['GET'])
def profile():
    res = None
    return render_template('profile.html', res=res)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
