import psycopg2
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/proyecto1dbp'
connection = psycopg2.connect('host=localhost port=5432 user=postgres password=password dbname=proyecto1dbp')
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False


class Usuario(db.Model):
    username = db.Column(db.String(32), primary_key=True)
    balance = db.Column(db.Integer, nullable=False)


class Juego(db.Model):
    nombre = db.Column(db.String(64), primary_key=True)


class Tienda(db.Model):
    nombre = db.Column(db.String(32), primary_key=True)


class Inventario(db.Model):
    j_nombre = db.Column(db.String(64), db.ForeignKey('juego.nombre'), primary_key=True)
    u_nombre = db.Column(db.String(32), db.ForeignKey('usuario.username'), nullable=False)


class Stock(db.Model):
    j_nombre = db.Column(db.String(64), db.ForeignKey('juego.nombre'), primary_key=True)
    t_nombre = db.Column(db.String(32), db.ForeignKey('tienda.nombre'), nullable=False)
    costo = db.Column(db.Float(precision=2), nullable=False)


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


@app.route('/initialize')
def initialize():
    cursor = connection.cursor()
    cursor.execute('INSERT INTO tienda (nombre) VALUES (\'steam\');'
                   'INSERT INTO tienda (nombre) VALUES (\'epic_games\');'
                   'INSERT INTO tienda (nombre) VALUES (\'battledotnet\');'
                   'INSERT INTO juego (nombre) VALUES (\'Counter-Strike: Global Offensive\');'
                   'INSERT INTO juego (nombre) VALUES (\'Dota 2\');'
                   'INSERT INTO juego (nombre) VALUES (\'PLAYERUNKNOWN\'\'S BATTLEGROUNDS\');'
                   'INSERT INTO juego (nombre) VALUES (\'Apex Legends\');'
                   'INSERT INTO juego (nombre) VALUES (\'Grand Theft Auto V\');'
                   'INSERT INTO stock (j_nombre,t_nombre,costo)'
                   ' VALUES (\'Counter-Strike: Global Offensive\',\'steam\',0);'
                   'INSERT INTO stock (j_nombre,t_nombre,costo) VALUES (\'Dota 2\',\'steam\',0);'
                   'INSERT INTO stock (j_nombre,t_nombre,costo)'
                   ' VALUES (\'PLAYERUNKNOWN\'\'S BATTLEGROUNDS\',\'steam\',52.00);'
                   'INSERT INTO stock (j_nombre,t_nombre,costo) VALUES (\'Apex Legends\',\'steam\',0);'
                   'INSERT INTO stock (j_nombre,t_nombre,costo) VALUES (\'Grand Theft Auto V\',\'steam\',49.17);'
                   'COMMIT;')
    return "inicializado"


if __name__ == '__main__':
    app.run(port=8080, threaded=True, host='127.0.0.1')
