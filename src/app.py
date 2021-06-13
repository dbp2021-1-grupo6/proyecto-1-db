from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import ValidationError

app = Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/proyecto1dbp'
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False


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
    return render_template('home.html')


@app.route('/games', methods=['GET'])
def print_tiendas():
    return render_template('game.html', data=Game.query.all())


@app.route('/inventory/<id>', methods=['GET'])
def print_stock(user_id):
    return render_template('stock.html', data=Inventory.query.filter_by(u_id=user_id).all())


@app.route('/register', methods=['GET', 'POST'])
def register_user_get():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        content = request.form
    if len(content['username']) > 32:
        raise ValidationError('Nombre del usuario es mayor al límite de 32 caracteres.')
    elif len(content['psw']) > 32:
        raise ValidationError('Contraseña mayor del límite de 32 caracteres.')
    elif content['psw'] is content['psw-repeat']:
        raise ValidationError('Contraseñas no coinciden.')
    elif Client.query.filter_by(username=content['username']).first() is not None:
        raise ValidationError('Nombre del usuario ya existe.')
    db.session.add(Client(username=content['username'], password=content['psw'], balance=200))
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port=8080, threaded=True, host='127.0.0.1')
