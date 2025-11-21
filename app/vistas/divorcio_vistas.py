from flask import request, jsonify
from app.models import divorcio_model
from sqlite3 import IntegrityError

REQUIRED_FIELDS = [
    "numero_expediente",
    "asunto_principal",
    "numero_folio",
    "numero_tomo",
    "fecha_registro_div",
    "lugar_registro_div",
    "id_empleado",
    "fecha_sentencia",
    "lugar_sentencia",
    "poder_judicial",
    "nombre_abogado",
    "numero_ipsa_abogado",
    "acta_matrimonio",
    "motivo",
]

UPDATE_FIELDS = [
    "lugar_sentencia", 
    "poder_judicial", 
    "asunto_principal", 
    "motivo", 
    "lugar_registro_div", 
    "nombre_abogado", 
    "numero_ipsa_abogado"
]


def setup_routes(divorcio_bp):
    @divorcio_bp.route("", methods=["POST"])
    def crear_divorcio():
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

        numero_expediente = data.get("numero_expediente")
        asunto_principal = data.get("asunto_principal")
        numero_folio = data.get("numero_folio")
        numero_tomo = data.get("numero_tomo")
        fecha_registro_div = data.get("fecha_registro_div")
        lugar_registro_div = data.get("lugar_registro_div")
        id_empleado = data.get("id_empleado")
        fecha_sentencia = data.get("fecha_sentencia")
        lugar_sentencia = data.get("lugar_sentencia")
        poder_judicial = data.get("poder_judicial")
        nombre_abogado = data.get("nombre_abogado")
        numero_ipsa_abogado = data.get("numero_ipsa_abogado")
        acta_matrimonio = data.get("acta_matrimonio")
        motivo = data.get("motivo")

        try:
            divorcio_model.crear_divorcio_db(
                numero_expediente,
                asunto_principal,
                numero_folio,
                numero_tomo,
                fecha_registro_div,
                lugar_registro_div,
                id_empleado,
                fecha_sentencia,
                lugar_sentencia,
                poder_judicial,
                nombre_abogado,
                numero_ipsa_abogado,
                acta_matrimonio,
                motivo,
            )

            return jsonify({"message": "Sentencia de divorcio creada."}), 201

        except IntegrityError as e:
            return (
                jsonify(
                    {
                        "error": "Error: La sentencia de divorcio ya existe.",
                        "detalle": f"Detalle DB: {e}",
                    }
                ),
                400,
            )

        except Exception as e:
            print(f"Error inesperado: {e}")
            return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500

    @divorcio_bp.route("/detalles", methods=["GET"])
    def listar_divorcios_completos():
        try:
            divorcios = divorcio_model.obtener_divorcios_con_matrimonio_y_ciudadanos()

            if not divorcios:
                return (
                    jsonify({"message": "No hay actas de divorcio registradas."}),
                    200,
                )

            return jsonify(divorcios), 200

        except Exception as e:
            print(f"Error al listar divorcios completos: {e}")
            return (
                jsonify({"error": "Error interno al obtener el listado de divorcios."}),
                500,
            )

    @divorcio_bp.route("/<int:sentencia_id>", methods=["GET"])
    def obtener_divorcio_por_id(sentencia_id):
        try:
            divorcio = divorcio_model.obtener_por_sentencia_divorcio(sentencia_id)

            if not divorcio:
                return (
                    jsonify(
                        {
                            "error": "Not Found",
                            "message": f"Sentencia de Divorcio N° {sentencia_id} no encontrada.",
                        }
                    ),
                    404,
                )

            return jsonify(divorcio), 200

        except Exception as e:
            print(f"Error al obtener divorcio por ID: {e}")
            return (
                jsonify({"error": "Error interno al obtener el registro de divorcio."}),
                500,
            )

    @divorcio_bp.route("/<int:sentencia_id>", methods=["PATCH"])
    def actualizar_divorcio(sentencia_id):
        data = request.get_json()

        if not data:
            return (
                jsonify(
                    {"error": "No se recibieron datos JSON para la actualización."}
                ),
                400,
            )

        missing_fields = [field for field in UPDATE_FIELDS if field not in data]
        if missing_fields:
            return (
                jsonify(
                    {
                        "error": "Faltan campos obligatorios para actualizar.",
                        "campos_faltantes": missing_fields,
                    }
                ),
                400,
            )

        try:
            divorcio_model.actualizar_divorcio_db(
                sentencia_id,
                data.get("lugar_sentencia"),
                data.get("poder_judicial"),
                data.get("asunto_principal"),
                data.get("motivo"),
                data.get("lugar_registro_div"),
                data.get("nombre_abogado"),
                data.get("numero_ipsa_abogado"),
            )

            return (
                jsonify(
                    {
                        "message": f"Sentencia de Divorcio N° {sentencia_id} actualizada correctamente."
                    }
                ),
                200,
            )

        except Exception as e:
            print(f"Error al actualizar divorcio: {e}")
            return (
                jsonify(
                    {"error": "Ocurrió un error interno durante la actualización."}
                ),
                500,
            )
