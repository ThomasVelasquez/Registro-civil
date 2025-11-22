from flask import request, jsonify
from app.models import empleado_model
from sqlite3 import IntegrityError

REQUIRED_FIELDS = [
    "id_ciudadano",
    "numero_empleado",
    "oficina_registro",
    "numero_resolucion",
    "fecha_resolucion",
    "numero_gaceta",
    "fecha_gaceta"
]


def setup_routes(empleado_bp):

    @empleado_bp.route("", methods=["POST"])
    def crear_empleado():
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se recibieron datos JSON."}), 400

        missing_fields = [
            field
            for field in REQUIRED_FIELDS
            if field not in data or data.get(field) is None
        ]

        if missing_fields:
            return (
                jsonify(
                    {
                        "error": "Faltan campos obligatorios.",
                        "campos_faltantes": missing_fields,
                    }
                ),
                400,
            )

        id_empleado = data.get("id_empleado")
        id_ciudadano = data.get("id_ciudadano")
        numero_empleado = data.get("numero_empleado")
        oficina_registro = data.get("oficina_registro")
        numero_resolucion = data.get("numero_resolucion")
        fecha_resolucion = data.get("fecha_resolucion")
        numero_gaceta = data.get("numero_gaceta")
        fecha_gaceta = data.get("fecha_gaceta")

        try:
            empleado_model.crear_empleado_db(
                id_empleado,
                id_ciudadano,
                numero_empleado,
                oficina_registro,
                numero_resolucion,
                fecha_resolucion,
                numero_gaceta,
                fecha_gaceta,
            )
            return jsonify({"message": "Empleado Creado."}), 201

        except IntegrityError as e:
            return (
                jsonify(
                    {
                        "error": "Error: La cédula ya existe.",
                        "detalle": f"Detalle DB: {e}",
                    }
                ),
                400,
            )

        except Exception as e:
            print(f"Error inesperado: {e}")
            return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500

    @empleado_bp.route("/", methods=["GET"])
    def listar_empleados():
        empleados = empleado_model.obtener_todos_empleados()
        return jsonify(empleados), 200
    
    @empleado_bp.route("/detalles", methods=["GET"])
    def listar_empleados_con_ciudadanos():
        try:
            empleados = empleado_model.obtener_empleados_con_ciudadanos()
            
            if not empleados:
                return jsonify({"message": "No hay empleados registrados."}), 200
                
            return jsonify(empleados), 200

        except Exception as e:
            print(f"Error al listar empleados con ciudadanos: {e}")
            return jsonify({"error": "Error interno al obtener el listado de empleados."}), 500
        

    @empleado_bp.route("/buscar_id", methods=["GET"])
    def buscar_id_empleado_por_numero():
        numero_empleado_str = request.args.get("numero") 

        if not numero_empleado_str:
            return jsonify({"error": "Parámetro 'numero' obligatorio."}), 400

        try:
            numero_empleado = int(numero_empleado_str)
        except ValueError:
            return jsonify({"error": "El 'numero' de empleado debe ser un número entero válido."}), 400

        try:
            id_empleado = empleado_model.obtener_id_por_numero(numero_empleado)
            
            if id_empleado is not None:
                return jsonify({
                    "message": "ID de empleado encontrado",
                    "numero_empleado": numero_empleado,
                    "id_empleado": id_empleado
                }), 200
            else:
                return jsonify({
                    "error": "Empleado no encontrado",
                    "numero_empleado": numero_empleado
                }), 404
        
        except Exception as e:
            print(f"Error al buscar ID de empleado por número: {e}")
            return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500