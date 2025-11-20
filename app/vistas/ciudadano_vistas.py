from flask import request, jsonify
from app.models import ciudadano_model
from sqlite3 import IntegrityError 

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

def setup_routes(ciudadano_bp):

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
        
        # Mantenemos la lógica de obtención de datos 
        cedula = data.get('cedula') or data.get('id_number')
        primer_nombre = data.get('primer_nombre') or data.get('first_name')
        segundo_nombre = data.get('segundo_nombre') or data.get('second_name')
        primer_apellido = data.get('primer_apellido') or data.get('first_lastName') or data.get('first_lastName')
        segundo_apellido = data.get('segundo_apellido') or data.get('second_lastName')
        genero = data.get('genero') or data.get('gender')
        nacionalidad = data.get('nacionalidad') or data.get('nationality')
        estado_civil = data.get('estado_civil') or data.get('civil_status')
        domicilio = data.get('domicilio') or data.get('address')
        fecha_nacimiento = data.get('fecha_nacimiento') or data.get('birth_date')
        profesion = data.get('profesion') or data.get('profession')
        
        try:
            ciudadano_model.crear_ciudadano_db(
                cedula, primer_nombre, segundo_nombre, primer_apellido, 
                segundo_apellido, genero, nacionalidad, estado_civil, 
                domicilio, fecha_nacimiento, profesion
            )
            return jsonify({"message": "Ciudadano creado."}), 201
            
        except IntegrityError as e:
            return jsonify({
                "error": "Error: La cédula ya existe.",
                "detalle": f"Detalle DB: {e}"
            }), 400
            
        except Exception as e:
            print(f"Error inesperado: {e}")
            return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500

    @ciudadano_bp.route('/', methods=['GET'])
    def listar_ciudadanos():
        ciudadanos = ciudadano_model.obtener_todos_ciudadanos()
        return jsonify(ciudadanos), 200

    @ciudadano_bp.route('/<int:id_ciudadano>', methods=['GET'])
    def obtener_ciudadano(id_ciudadano):
        ciudadano = ciudadano_model.obtener_ciudadano_por_id(id_ciudadano)
        
        if ciudadano:
            return jsonify(ciudadano), 200
        return jsonify({"message": "Ciudadano no encontrado."}), 404

    @ciudadano_bp.route('/<int:id_ciudadano>', methods=['PUT'])
    def actualizar_ciudadano(id_ciudadano):
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se recibieron datos JSON para actualizar."}), 400

        cedula = data.get('cedula') or data.get('id_number')
        primer_nombre = data.get('primer_nombre') or data.get('first_name')
        segundo_nombre = data.get('segundo_nombre') or data.get('second_name')
        primer_apellido = data.get('primer_apellido') or data.get('first_lastName') or data.get('first_lastName')
        segundo_apellido = data.get('segundo_apellido') or data.get('second_lastName')
        genero = data.get('genero') or data.get('gender')
        nacionalidad = data.get('nacionalidad') or data.get('nationality')
        estado_civil = data.get('estado_civil') or data.get('civil_status')
        domicilio = data.get('domicilio') or data.get('address')
        fecha_nacimiento = data.get('fecha_nacimiento') or data.get('birth_date')
        profesion = data.get('profesion') or data.get('profession')
        
        try:
            ciudadano_model.actualizar_ciudadano_db(
                cedula, primer_nombre, segundo_nombre, primer_apellido, 
                segundo_apellido, genero, nacionalidad, estado_civil, 
                domicilio, fecha_nacimiento, profesion
            )
            return jsonify({"message": f"Ciudadano {id_ciudadano} actualizado."}), 200
        except IntegrityError as e:
            return jsonify({
                "error": "Error de integridad al actualizar. Revise que los campos obligatorios estén presentes y no sean NULL.",
                "detalle": f"Detalle DB: {e}"
            }), 400
        except Exception as e:
            return jsonify({"error": "Error al actualizar.", "detalle_tecnico": str(e)}), 500