import psycopg2
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/proyecto1dbp'
connection = psycopg2.connect('host=localhost port=5432 user=postgres password=password dbname=proyecto1dbp')
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    balance = db.Column(db.Integer, nullable=False)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Integer, nullable=False)


class Inventory(db.Model):
    g_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


db.create_all()


@app.route('/tiendas')
def print_tiendas():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tienda')
    data = cursor.fetchall()
    return render_template('tienda.html', data=data)


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


@app.route('/register')
def registerUser():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    content = request.json
    print(request)


@app.route('/initialize')
def initialize():
    cursor = connection.cursor()
    cursor.execute('INSERT INTO game (name,category,price)'
                   ' VALUES (\'Counter-Strike: Global Offensive\',\'First Person Shooter\',0);'
                   'INSERT INTO game (name,category,price)'
                   ' VALUES (\'Dota 2\',\'MOBA\',10);'
                   'INSERT INTO game (name,category,price)'
                   ' VALUES (\'PLAYERUNKNOWN\'\'S BATTLEGROUNDS\',\'Battle Royale\',60);'
                   'INSERT INTO game (name,category,price)'
                   ' VALUES (\'Apex Legends\',\'First Person Shooter\',20);'
                   'INSERT INTO game (name,category,price)'
                   ' VALUES (\'Grand Theft Auto V\',\'Open World\',100);'
                   'COMMIT;')
    return "inicializado"


if __name__ == '__main__':
    app.run(port=8080, threaded=True, host='127.0.0.1')
