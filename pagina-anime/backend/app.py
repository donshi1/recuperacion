import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_talisman import Talisman
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)
Talisman(app)

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")
supabase: Client = None
if url and key:
    supabase = create_client(url, key)

PRODUCTOS_DB = {
    1: {'nombre': 'Figura Goku SSJ', 'precio': 1500.0, 'imagen': 'goku.jpg'},
    2: {'nombre': 'Manga One Piece Vol. 1', 'precio': 250.0, 'imagen': 'onepiece.jpg'}
}

@app.route('/api/productos', methods=['GET'])
def get_productos():
    productos_lista = [{'id': k, **v} for k, v in PRODUCTOS_DB.items()]
    return jsonify(productos_lista)

@app.route('/api/pagar', methods=['POST'])
def procesar_pago():
    if not supabase:
        return jsonify({"error": "Error de conexion con la base de datos"}), 500
    
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Acceso denegado. Se requiere autenticacion."}), 401

    datos_compra = request.json
  
    carrito = datos_compra.get("carrito", [])
    if not carrito:
        return jsonify({"error": "El carrito esta vacio"}), 400

    monto_total = 0.0
    nombres_comprados = []
    
    for item_id in carrito:
        producto = PRODUCTOS_DB.get(item_id)
        if producto:
            monto_total += producto['precio']
            nombres_comprados.append(producto['nombre'])

    concepto = f"Compra: {', '.join(nombres_comprados)}"

    return jsonify({
        "mensaje": "Pago procesado correctamente",
        "estado": "AUTHORIZED",
        "monto": monto_total,
        "concepto": concepto
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
