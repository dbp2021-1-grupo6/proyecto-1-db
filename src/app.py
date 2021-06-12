import psycopg2
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import ValidationError

app = Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/proyecto1dbp'
connection = psycopg2.connect('host=localhost port=5432 user=postgres password=password dbname=proyecto1dbp')
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    balance = db.Column(db.Integer, nullable=False)


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


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/games')
def print_tiendas():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM game')
    data = cursor.fetchall()
    return render_template('game.html', data=data)


@app.route('/tiendas/<name>')
def print_stock(name):
    cursor = connection.cursor()
    cursor.execute('SELECT j.nombre, s.costo '
                   'FROM juego j '
                   'INNER JOIN stock s '
                   'ON s.j_nombre = j.nombre '
                   'WHERE s.t_nombre = \''+str(name)+'\';')
    data = cursor.fetchall()
    return render_template('stock.html', data=data)


@app.route('/register', methods=['GET'])
def registerUserGet():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def registerUserPost():
    content = request.form
    if len(content['username']) > 32:
        raise ValidationError('Nombre del usuario es mayor al límite de 32 caracteres.')
    elif len(content['password']) > 32:
        raise ValidationError('Contraseña mayor del límite de 32 caracteres.')
    elif content['psw'] is not content['psw-repeat']:
        raise ValidationError('Contraseñas no coinciden.')
    elif Client.query.filter_by(username=content['username']).first() is not None:
        raise ValidationError('Nombre del usuario ya existe.')
    db.session.add(Client(username=content['username'], password=content['psw'], balance=200))
    return 'Otro usuario registrado'


@app.route('/init')
def initialize():
    cursor = connection.cursor()
    cursor.execute('INSERT INTO game (name,category,price)'
                   ' VALUES (\'Counter-Strike: Global Offensive\',\'First Person Shooter\',0);'
                   'INSERT INTO game (name,category,price)'
                   ' VALUES (\'Dota 2\',\'MOBA\',10.50);'
                   'INSERT INTO game (name,category,price)'
                   ' VALUES (\'PLAYERUNKNOWN\'\'S BATTLEGROUNDS\',\'Battle Royale\',60.90);'
                   'INSERT INTO game (name,category,price)'
                   ' VALUES (\'Apex Legends\',\'First Person Shooter\',20.80);'
                   'INSERT INTO game (name,category,price)'
                   ' VALUES (\'Grand Theft Auto V\',\'Open World\',100.00);'
                   'COMMIT;')
    return "inicializado"


if __name__ == '__main__':
    app.run(port=8080, threaded=True, host='127.0.0.1')
