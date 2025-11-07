from flask import Blueprint, request, jsonify
from app.models import ciudadano_model
from sqlite3 import IntegrityError 

ciudadano_bp = Blueprint('ciudadanos', __name__)

REQUIRED_FIELDS = [
    'cedula', 
    'primer_nombre', 
    'primer_apellido', 
    'genero', 
    'nacionalidad', 
    'estado_civil', 
    'domicilio',
    'fecha_nacimiento',
    'profesion'
]

@ciudadano_bp.route('', methods=['POST'])

def crear_ciudadano():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON"}), 400

    missing_fields = [field for field in REQUIRED_FIELDS if field not in data or data.get(field) is None]
    
    if missing_fields:
        return jsonify({
            "error": "Faltan campos obligatorios.",
            "campos_faltantes": missing_fields
        }), 400

    
    """ cedula = data.get('cedula')
    primer_nombre = data.get('primer_nombre')
    segundo_nombre = data.get('segundo_nombre') 
    primer_apellido = data.get('primer_apellido')
    segundo_apellido = data.get('segundo_apellido') 
    genero = data.get('genero')
    nacionalidad = data.get('nacionalidad')
    estado_civil = data.get('estado_civil')
    domicilio = data.get('domicilio')
    fecha_nacimiento = data.get('fecha_nacimiento')
    profesion = data.get('profesion') """
    
    cedula = data.get('cedula') or data.get('id_number')
    primer_nombre = data.get('primer_nombre') or data.get('first_name')
    segundo_nombre = data.get('segundo_nombre') or data.get('second_name')
    primer_apellido = data.get('primer_apellido') or data.get('first_lastName') or data.get('first_lastname')
    segundo_apellido = data.get('segundo_apellido') or data.get('second_lastName')
    genero = data.get('genero') or data.get('gender')
    nacionalidad = data.get('nacionalidad') or data.get('nationality')
    estado_civil = data.get('estado_civil') or data.get('civilStatus')
    domicilio = data.get('domicilio') or data.get('address')
    fecha_nacimiento = data.get('fecha_nacimiento') or data.get('birthDate')
    profesion = data.get('profesion') or data.get('profession')
    
    
    try:
        ciudadano_model.crear_ciudadano_db(
            cedula, primer_nombre, segundo_nombre, primer_apellido, 
            segundo_apellido, genero, nacionalidad, estado_civil, 
            domicilio, fecha_nacimiento, profesion
        )
        return jsonify({"message": "Ciudadano creado"}), 201
        
    except IntegrityError as e:
        return jsonify({
            "error": "Error: La cédula ya existe",
            "detalle": f"Detalle DB: {e}"
        }), 400
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500

@ciudadano_bp.route('/', methods=['GET'])
def listar_ciudadanos():
    ciudadanos = ciudadano_model.obtener_todos_ciudadanos()
    return jsonify(ciudadanos), 200

@ciudadano_bp.route('/<int:cedula>', methods=['GET'])
def obtener_ciudadano(cedula):
    ciudadano = ciudadano_model.obtener_ciudadano_por_cedula(cedula)
    
    if ciudadano:
        return jsonify(ciudadano), 200
    return jsonify({"message": "Ciudadano no encontrado"}), 404

@ciudadano_bp.route('/<int:cedula>', methods=['PUT'])
def actualizar_ciudadano(cedula):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos JSON para actualizar"}), 400

    primer_nombre = data.get('primer_nombre')
    segundo_nombre = data.get('segundo_nombre')
    primer_apellido = data.get('primer_apellido')
    segundo_apellido = data.get('segundo_apellido')
    genero = data.get('genero')
    nacionalidad = data.get('nacionalidad')
    estado_civil = data.get('estado_civil')
    domicilio = data.get('domicilio')
    fecha_nacimiento = data.get('fecha_nacimiento')
    profesion = data.get('profesion')
    
    try:
        ciudadano_model.actualizar_ciudadano_db(
            cedula, primer_nombre, segundo_nombre, primer_apellido, 
            segundo_apellido, genero, nacionalidad, estado_civil, 
            domicilio, fecha_nacimiento, profesion
        )
        return jsonify({"message": f"Ciudadano {cedula} actualizado"}), 200
    except IntegrityError as e:
         return jsonify({
            "error": "Error de integridad al actualizar. Revise que los campos obligatorios estén presentes y no sean NULL.",
            "detalle": f"Detalle DB: {e}"
        }), 400
    except Exception:
        return jsonify({"error": "Error al actualizar."}), 500

""" @ciudadano_bp.route('/<int:cedula>', methods=['DELETE'])
def eliminar_ciudadano(cedula):
    ciudadano_model.eliminar_ciudadano_db(cedula)
    return jsonify({"message": f"Ciudadano {cedula} eliminado"}), 204 """