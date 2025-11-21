from flask import request, jsonify
from app.models import matrimonio_model
from sqlite3 import IntegrityError

REQUIRED_FIELDS = [
    "numero_folio",
    "numero_tomo",
    "fecha_registro_mat",
    "lugar_registro_mat",
    "id_empleado",
    "fecha_matrimonio",
    "lugar_matrimonio",
    "hora_matrimonio",
    "id_ciudadanoC1",
    "id_ciudadanoC2",
    "id_ciudadanoMC1",
    "id_ciudadanoPC1",
    "id_ciudadanoMC2",
    "id_ciudadanoPC2",
    "id_ciudadanoMT1",
    "id_ciudadanoMT2",
]


def setup_routes(matrimonio_bp):

    @matrimonio_bp.route("", methods=["POST"])
    def crear_matrimonio():
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
        acta_matrimonio = data.get("acta_matrimonio")
        numero_folio = data.get("numero_folio")
        numero_tomo = data.get("numero_tomo")
        fecha_registro_mat = data.get("fecha_registro_mat")
        lugar_registro_mat = data.get("lugar_registro_mat")
        id_empleado = data.get("id_empleado")
        fecha_matrimonio = data.get("fecha_matrimonio")
        lugar_matrimonio = data.get("lugar_matrimonio")
        hora_matrimonio = data.get("hora_matrimonio")
        id_ciudadanoC1 = data.get("id_ciudadanoC1")
        id_ciudadanoC2 = data.get("id_ciudadanoC2")
        id_ciudadanoMC1 = data.get("id_ciudadanoMC1")
        id_ciudadanoPC1 = data.get("id_ciudadanoPC1")
        id_ciudadanoMC2 = data.get("id_ciudadanoMC2")
        id_ciudadanoPC2 = data.get("id_ciudadanoPC2")
        id_ciudadanoMT1 = data.get("id_ciudadanoMT1")
        id_ciudadanoMT2 = data.get("id_ciudadanoMT2")

        print(
            "datas",
            acta_matrimonio,
            numero_folio,
            numero_tomo,
            fecha_registro_mat,
            lugar_registro_mat,
            id_empleado,
            fecha_matrimonio,
            lugar_matrimonio,
            hora_matrimonio,
            id_ciudadanoC1,
            id_ciudadanoC2,
            id_ciudadanoMC1,
            id_ciudadanoPC1,
            id_ciudadanoMC2,
            id_ciudadanoPC2,
            id_ciudadanoMT1,
            id_ciudadanoMT2,
        )

        try:
            matrimonio_model.crear_matrimonio_db(
                acta_matrimonio,
                numero_folio,
                numero_tomo,
                fecha_registro_mat,
                lugar_registro_mat,
                id_empleado,
                fecha_matrimonio,
                lugar_matrimonio,
                hora_matrimonio,
                id_ciudadanoC1,
                id_ciudadanoC2,
                id_ciudadanoMC1,
                id_ciudadanoPC1,
                id_ciudadanoMC2,
                id_ciudadanoPC2,
                id_ciudadanoMT1,
                id_ciudadanoMT2,
            )
            return jsonify({"message": "Acta de matrimonio creada."}), 201

        except IntegrityError as e:
            return (
                jsonify(
                    {
                        "error": "Error: El acta de matrimonio ya existe.",
                        "detalle": f"Detalle DB: {e}",
                    }
                ),
                400,
            )

        except Exception as e:
            print(f"Error inesperado: {e}")
            return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500

    @matrimonio_bp.route("/", methods=["GET"])
    def listar_matrimonios():
        matrimonios = matrimonio_model.obtener_los_matrimonios()
        return jsonify(matrimonios), 200

    @matrimonio_bp.route("/<int:acta_matrimonio>", methods=["GET"])
    def listar_por_acta(acta_matrimonio):
        matrimonio = matrimonio_model.obtener_matrimonio_por_acta(acta_matrimonio)
        return jsonify(matrimonio), 200

    @matrimonio_bp.route("/<int:acta_matrimonio>", methods=["PUT"])
    def actualizar_acta(acta_matrimonio):
        data = request.get_json()

        campos_requeridos = [
            "acta_matrimonio",
            "numero_folio",
            "numero_tomo",
            "fecha_registro_mat",
            "lugar_registro_mat",
            "id_empleado",
            "fecha_matrimonio",
            "lugar_matrimonio",
            "hora_matrimonio",
            "id_ciudadanoC1",
            "id_ciudadanoC2",
            "id_ciudadanoMC1",
            "id_ciudadanoPC1",
            "id_ciudadanoMC2",
            "id_ciudadanoPC2",
            "id_ciudadanoMT1",
            "id_ciudadanoMT2",
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
        fecha_registro_mat = data.get("fecha_registro_mat")
        lugar_registro_mat = data.get("lugar_registro_mat")
        id_empleado = data.get("id_empleado")
        fecha_matrimonio = data.get("fecha_matrimonio")
        lugar_matrimonio = data.get("lugar_matrimonio")
        hora_matrimonio = data.get("hora_matrimonio")
        id_ciudadanoC1 = data.get("id_ciudadanoC1")
        id_ciudadanoC2 = data.get("id_ciudadanoC2")
        id_ciudadanoMC1 = data.get("id_ciudadanoMC1")
        id_ciudadanoPC1 = data.get("id_ciudadanoPC1")
        id_ciudadanoMC2 = data.get("id_ciudadanoMC2")
        id_ciudadanoPC2 = data.get("id_ciudadanoPC2")
        id_ciudadanoMT1 = data.get("id_ciudadanoMT1")
        id_ciudadanoMT2 = data.get("id_ciudadanoMT2")

        try:
            matrimonio_model.actualizar_matrimonio_db(
                acta_matrimonio,
                numero_folio,
                numero_tomo,
                fecha_registro_mat,
                lugar_registro_mat,
                id_empleado,
                fecha_matrimonio,
                lugar_matrimonio,
                hora_matrimonio,
                id_ciudadanoC1,
                id_ciudadanoC2,
                id_ciudadanoMC1,
                id_ciudadanoPC1,
                id_ciudadanoMC2,
                id_ciudadanoPC2,
                id_ciudadanoMT1,
                id_ciudadanoMT2,
            )

            return jsonify({"Message": f"Acta {acta_matrimonio} actualizada."})
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

    @matrimonio_bp.route("/actas", methods=["GET"])
    def listar_matrimonios_con_ciudadanos():
        try:
            matrimonios = matrimonio_model.obtener_matrimonios_con_ciudadanos()
            
            if not matrimonios:
                return jsonify({"message": "No hay actas de matrimonio registradas."}), 200
                
            return jsonify(matrimonios), 200

        except Exception as e:
            print(f"Error al listar matrimonios con ciudadanos: {e}")
            return jsonify({"error": "Error interno al obtener las actas."}), 500
