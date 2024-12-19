from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'  # Cambiado a SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la tabla productos
class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    stock_inicial = db.Column(db.Integer, nullable=False)
    stock_actual = db.Column(db.Integer, nullable=False)
    proveedor = db.Column(db.String(255))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    rfid = db.Column(db.String(50), unique=True, nullable=False)
    unidad_medida = db.Column(db.String(50))
    estado = db.Column(db.String(50), default='Activo')
    ubicacion = db.Column(db.String(255))
    imagen_url = db.Column(db.Text)
    fecha_vencimiento = db.Column(db.Date)
    nivel_reorden = db.Column(db.Integer, default=0)
    notas = db.Column(db.Text)

class Movimiento(db.Model):
    __tablename__ = 'movimientos'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'entrada' o 'salida'
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.Column(db.String(255), nullable=True)
    nota = db.Column(db.Text)

# Endpoint para registrar un producto
@app.route('/api/productos', methods=['POST'])
def registrar_producto():
    data = request.get_json()
    try:
        nuevo_producto = Producto(
            nombre=data['nombre'],
            categoria=data.get('categoria'),
            descripcion=data.get('descripcion'),
            precio_unitario=data['precio_unitario'],
            stock_inicial=data['stock_inicial'],
            stock_actual=data['stock_inicial'],
            proveedor=data.get('proveedor'),
            rfid=data['rfid'],
            unidad_medida=data.get('unidad_medida'),
            estado=data.get('estado', 'Activo'),
            ubicacion=data.get('ubicacion'),
            imagen_url=data.get('imagen_url'),
            fecha_vencimiento=data.get('fecha_vencimiento'),
            nivel_reorden=data.get('nivel_reorden', 0),
            notas=data.get('notas')
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return jsonify({"message": "Producto registrado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Endpoint para registrar RFID
@app.route('/api/register_rfid', methods=['POST'])
def procesar_rfid():
    data = request.get_json()
    rfid_code = data.get("rfid")

    if not rfid_code:
        return jsonify({"error": "Código RFID no proporcionado"}), 400

    producto = Producto.query.filter_by(rfid=rfid_code).first()
    if not producto:
        return jsonify({"error": "RFID no asociado a ningún producto"}), 404

    if producto.stock_actual > 0:
        producto.stock_actual -= 1
        movimiento = Movimiento(
            producto_id=producto.id,
            tipo="salida",
            cantidad=1,
            usuario="Sensor RFID",
            nota=f"Salida automática por RFID {rfid_code}"
        )
        db.session.add(movimiento)
        db.session.commit()
        return jsonify({"message": f"Producto {producto.nombre} actualizado. Stock actual: {producto.stock_actual}"}), 200
    else:
        return jsonify({"error": f"Producto {producto.nombre} sin stock disponible"}), 400

# Otros endpoints omitidos por espacio...

# Endpoint para servir el frontend
@app.route("/")
def servir_frontend():
    return send_from_directory("frontend", "index.html")

@app.route("/frontend/<path:path>")
def servir_estaticos(path):
    return send_from_directory("frontend", path)

if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", port=80)
