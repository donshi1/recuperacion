from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tienda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen = db.Column(db.String(200), nullable=False)

@app.route('/api/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    return jsonify([{'id': p.id, 'nombre': p.nombre, 'precio': p.precio, 'imagen': p.imagen} for p in productos])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Producto.query.first():
            db.session.add(Producto(nombre="Figura Goku SSJ", precio=1500.0, imagen="goku.jpg"))
            db.session.add(Producto(nombre="Manga One Piece Vol. 1", precio=250.0, imagen="onepiece.jpg"))
            db.session.commit()
    app.run(host='0.0.0.0', port=5000)
