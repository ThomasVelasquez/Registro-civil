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
    "fecha_sentencia_div",
    "lugar_sentencia_div",
    "hora_sentencia_div",
    "causa_divorcio",
    "poder_judicial",
    "nombre_abogado",
    "numero_ipsa",
    "acta_matrimonio",
    "motivo",
    "id_ciudadano_1",
    "id_ciudadano_2",
    "id_empleado",
]


def setup_routes(divorcio_bp):
    @divorcio_bp.route("", methods=["POST"])
    def crear_divorcio():
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se recibieron datos JSON"}), 400

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
        fecha_sentencia_div = data.get("fecha_sentencia_div")
        lugar_sentencia_div = data.get("lugar_sentencia_div")
        hora_sentencia_div = data.get("hora_sentencia_div")
        causa_divorcio = data.get("causa_divorcio")
        poder_judicial = data.get("poder_judicial")
        nombre_abogado = data.get("nombre_abogado")
        numero_ipsa = data.get("numero_ipsa")
        acta_matrimonio = data.get("acta_matrimonio")
        motivo = data.get("motivo")
        id_ciudadano_1 = data.get("id_ciudadano_1")
        id_ciudadano_2 = data.get("id_ciudadano_2")

        try:
            divorcio_model.crear_divorcio_db(
                numero_expediente,
                asunto_principal,
                numero_folio,
                numero_tomo,
                fecha_registro_div,
                lugar_registro_div,
                fecha_sentencia_div,
                lugar_sentencia_div,
                hora_sentencia_div,
                causa_divorcio,
                poder_judicial,
                nombre_abogado,
                numero_ipsa,
                acta_matrimonio,
                motivo,
                id_ciudadano_1,
                id_ciudadano_2,
                id_empleado
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
