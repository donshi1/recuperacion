import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_talisman import Talisman
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)
Talisman(app)

url: str = os.environ.get("https://ygvzhdhxmjprkjaxgoaj.supabase.co", "")
key: str = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlndnpoZGh4bWpwcmtqYXhnb2FqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc2ODQ5NTksImV4cCI6MjEwMzI2MDk1OX0.I6AQpVjlF8rHqjDx0ZYUa66Q-G9v9nLiAwtDf13uI-o", "")
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
