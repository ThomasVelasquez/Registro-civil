from flask import request, jsonify
from app.models import nacimiento_model
from sqlite3 import IntegrityError

REQUIRED_FIELDS = [
    "numero_folio",
    "numero_tomo",
    "fecha_registro_nac",
    "lugar_registro_nac",
    "lugar_nacimiento",
    "hora_nacimiento",
    "nro_certificado_medico",
    "fecha_expedicion_cert",
    "autoridad_expide_cert",
    "numero_mpps_autoridad",
    "nombre_centro_salud",
    "documentos_presentandos",
    "id_ciudadano",
    "id_empleado",
    "id_ciudadanoM",
    "id_ciudadanoP",
    "id_ciudadanoNT1",
    "id_ciudadanoNT2",
]


def setup_routes(nacimiento_bp):

    @nacimiento_bp.route("", methods=["POST"])
    def crear_nacimiento():
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

        numero_folio = data.get("numero_folio")
        numero_tomo = data.get("numero_tomo")
        fecha_registro_nac = data.get("fecha_registro_nac")
        lugar_registro_nac = data.get("lugar_registro_nac")
        lugar_nacimiento = data.get("lugar_nacimiento")
        hora_nacimiento = data.get("hora_nacimiento")
        nro_certificado_medico = data.get("nro_certificado_medico")
        fecha_expedicion_cert = data.get("fecha_expedicion_cert")
        autoridad_expide_cert = data.get("autoridad_expide_cert")
        numero_mpps_autoridad = data.get("numero_mpps_autoridad")
        nombre_centro_salud = data.get("nombre_centro_salud")
        documentos_presentandos = data.get("documentos_presentandos")
        id_ciudadano = data.get("id_ciudadano")
        id_empleado = data.get("id_empleado")
        id_ciudadanoM = data.get("id_ciudadanoM")
        id_ciudadanoP = data.get("id_ciudadanoP")
        id_ciudadanoNT1 = data.get("id_ciudadanoNT1")
        id_ciudadanoNT2 = data.get("id_ciudadanoNT2")

        try:
            nacimiento_model.crear_nacimiento_db(
                numero_folio,
                numero_tomo,
                fecha_registro_nac,
                lugar_registro_nac,
                lugar_nacimiento,
                hora_nacimiento,
                nro_certificado_medico,
                fecha_expedicion_cert,
                autoridad_expide_cert,
                numero_mpps_autoridad,
                nombre_centro_salud,
                documentos_presentandos,
                id_ciudadano,
                id_empleado,
                id_ciudadanoM,
                id_ciudadanoP,
                id_ciudadanoNT1,
                id_ciudadanoNT2,
            )
            return jsonify({"message": "Acta de nacimiento creada."}), 201

        except IntegrityError as e:
            return (
                jsonify(
                    {
                        "error": "Error: El acta de nacimiento ya existe.",
                        "detalle": f"Detalle DB: {e}",
                    }
                ),
                400,
            )

        except Exception as e:
            print(f"Error inesperado: {e}")
            return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500

    @nacimiento_bp.route("/", methods=["GET"])
    def listar_nacimientos():
        nacimientos = nacimiento_model.obtener_los_nacimientos()
        return jsonify(nacimientos), 200

    @nacimiento_bp.route("/<int:acta_nacimiento>", methods=["GET"])
    def listar_por_acta(acta_nacimiento):
        nacimiento = nacimiento_model.obtener_nacimiento_por_acta(acta_nacimiento)
        return jsonify(nacimiento), 200

    @nacimiento_bp.route("/<int:acta_nacimiento>", methods=["PUT"])
    def actualizar_acta(acta_nacimiento):
        data = request.get_json()

        campos_requeridos = [
            "numero_folio",
            "numero_tomo",
            "fecha_registro_nac",
            "lugar_registro_nac",
            "lugar_nacimiento",
            "hora_nacimiento",
            "nro_certificado_medico",
            "id_ciudadano",
            "id_empleado",
            "id_ciudadanoM",
            "id_ciudadanoP",
            "id_ciudadanoNT1",
            "id_ciudadanoNT2",
        ]

        for campo in campos_requeridos:
            if data.get(campo) is None:
                return (
                    jsonify(
                        {
                            "Error": f"El campo '{campo}' es obligatorio y no fue proporcionado o es nulo."
                        }
                    ),
                    400,
                )

        if not data:
            return (
                jsonify({"Error": "No se recibieron datos JSON para actualizar."}),
                400,
            )

        numero_folio = data.get("numero_folio")
        numero_tomo = data.get("numero_tomo")
        fecha_registro_nac = data.get("fecha_registro_nac")
        lugar_registro_nac = data.get("lugar_registro_nac")
        lugar_nacimiento = data.get("lugar_nacimiento")
        hora_nacimiento = data.get("hora_nacimiento")
        nro_certificado_medico = data.get("nro_certificado_medico")
        fecha_expedicion_cert = data.get("fecha_expedicion_cert")
        autoridad_expide_cert = data.get("autoridad_expide_cert")
        numero_mpps_autoridad = data.get("numero_mpps_autoridad")
        nombre_centro_salud = data.get("nombre_centro_salud")
        documentos_presentandos = data.get("documentos_presentandos")
        id_ciudadano = data.get("id_ciudadano")
        id_empleado = data.get("id_empleado")
        id_ciudadanoM = data.get("id_ciudadanoM")
        id_ciudadanoP = data.get("id_ciudadanoP")
        id_ciudadanoNT1 = data.get("id_ciudadanoNT1")
        id_ciudadanoNT2 = data.get("id_ciudadanoNT2")

        try:
            nacimiento_model.actualizar_nacimiento_db(
                acta_nacimiento,
                numero_folio,
                numero_tomo,
                fecha_registro_nac,
                lugar_registro_nac,
                lugar_nacimiento,
                hora_nacimiento,
                nro_certificado_medico,
                fecha_expedicion_cert,
                autoridad_expide_cert,
                numero_mpps_autoridad,
                nombre_centro_salud,
                documentos_presentandos,
                id_ciudadano,
                id_empleado,
                id_ciudadanoM,
                id_ciudadanoP,
                id_ciudadanoNT1,
                id_ciudadanoNT2,
            )

            return jsonify({"Message": f"Acta {acta_nacimiento} actualizada."})
        except IntegrityError as e:
            return (
                jsonify(
                    {
                        "error": "Error de integridad al actualizar. Revise que los campos obligatorios estén presentes y no sean NULL.",
                        "detalle": f"Detalle DB: {e}",
                    }
                ),
                400,
            )
        except Exception as e:
            return (
                jsonify({"error": "Error al actualizar.", "detalle_tecnico": str(e)}),
                500,
            )
