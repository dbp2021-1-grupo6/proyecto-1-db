from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/proyecto1dbp'
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False


class Usuario (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    balance = db.Column(db.Integer, nullable=False)


class Objeto (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), unique=True, nullable=False)
    juego = db.Column(db.String(32), nullable=False)
    url = db.Column(db.String(128), unique=True, nullable=False)


class Tienda (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), unique=True, nullable=False)


db.create_all()


class Inventario(db.Model):
    o_id = db.Column(db.Integer, db.ForeignKey('objeto.id'), primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True, nullable=False)


class Stock(db.Model):
    o_id = db.Column(db.Integer, db.ForeignKey('objeto.id'), primary_key=True)
    t_id = db.Column(db.Integer, db.ForeignKey('tienda.id'), nullable=False)
    costo = db.Column(db.Float(precision=2), nullable=False)


db.create_all()


@app.route('/tiendas')
def print_tiendas():
    data = db.session.query(Tienda).all()
    return render_template('tienda.html', data=data)


@app.route('/tiendas/<name>')
def print_stock(name):
    tienda = Tienda.query.filter_by(nombre=name).first()
    data = Stock.query.filter_by(t_id=tienda.id).all()
    return render_template('tienda.html', data=data)


if __name__ == '__main__':
    app.run(port=8080, threaded=True, host='127.0.0.1')
