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

@app.route('/api/productos', methods=['GET'])
def get_productos():
    productos = [
        {'id': 1, 'nombre': 'Figura Goku SSJ', 'precio': 1500.0, 'imagen': 'goku.jpg'},
        {'id': 2, 'nombre': 'Manga One Piece Vol. 1', 'precio': 250.0, 'imagen': 'onepiece.jpg'}
    ]
    return jsonify(productos)

@app.route('/api/pagar', methods=['POST'])
def procesar_pago():
    if not supabase:
        return jsonify({"error": "Error de conexion con la base de datos"}), 500
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Acceso denegado. Se requiere autenticacion."}), 401
 
    datos_compra = request.json
    

    
    return jsonify({
        "mensaje": "Pago procesado correctamente",
        "estado": "AUTHORIZED",
        "monto": datos_compra.get("monto", 0)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
