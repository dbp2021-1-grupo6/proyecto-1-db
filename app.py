import json
import werkzeug
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lxolkxyqsxdjei:97f8d772cdfaf829a26c90116c15791892d9a4f162b7681773ca9fbc697fe3ef@ec2-34-194-130-103.compute-1.amazonaws.com:5432/ddvm984l3tlkav'
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


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return render_template('errorManager.html')


app.register_error_handler(404, handle_bad_request)
app.register_error_handler(500, handle_bad_request)


@app.route('/')
def redirect_home():
    return redirect(url_for('home'))


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html', res=None)


@app.route('/games', methods=['GET', 'POST'])
def games():
    if request.method == 'GET':
        return render_template('game.html', res=None,  data=Game.query.all())
    else:
        content = json.loads(request.data)
        login_id = Client.query.filter_by(username=content['name']).first().id
        if Inventory.query.filter_by(c_id=login_id, g_id=content['id']).first() is not None:
            flash('Juego ya comprado')
            return redirect(url_for('games'))
        elif Client.query.filter_by(id=login_id).first().balance < Game.query.filter_by(id=content['id']).first().price:
            flash('Fondos Insuficientes')
            return redirect(url_for('games'))
        else:
            client = Client.query.filter_by(id=login_id).first()
            client.balance -= Game.query.filter_by(id=content['id']).first().price
            db.session.add(Inventory(g_id=content['id'], c_id=login_id))
            db.session.commit()
            db.session.close()
            return json.dumps({'message': "ok"})


@app.route('/inventory/<username>', methods=['GET', 'DELETE'])
def print_stock(username):
    if request.method == 'GET':
        user_id = Client.query.filter_by(username=username).first().id
        if user_id is not None:
            return render_template('inventory.html', res=None, data=db.session.query(Game)
                                   .join(Inventory)
                                   .filter(Game.id == Inventory.g_id, Inventory.c_id == user_id).all())
        else:
            return redirect(url_for('home'))
    else:
        content = json.loads(request.data)
        login_id = Client.query.filter_by(username=content['name']).first().id
        Inventory.query.filter_by(c_id=login_id, g_id=content['id']).delete()
        db.session.commit()
        db.session.close()
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
            flash("Las contrase??as no coinciden")
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
    if request.method == 'POST':
        content = request.form
        client = Client.query.filter_by(username=content['username']).first()
        if client is not None:
            if client.password == content['psw']:
                res = {'username': content['username']}
                return render_template('home.html', res=res)
            else:
                flash("Contrase??a Incorrecta")
                return redirect(url_for('login'))
        else:
            flash("Usuario no existente")
            return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    if request.method == 'GET':
        balance = Client.query.filter_by(username=username).first().balance
        return render_template('profile.html', res=None, usrnm=username, bal=balance)
    else:
        if request.form['monto'] != '' and float(request.form['monto']) > 0:
            client = Client.query.filter_by(username=username).first()
            client.balance += float(request.form['monto'])
            db.session.commit()
            db.session.close()
            flash('Fondos a??adidos')
        return redirect(url_for('profile', username=username))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
