from flask import request, jsonify, Blueprint
from app.models import matrimonio_model
from sqlite3 import IntegrityError

matrimonio_bp = Blueprint("matrimonio_bp", __name__, url_prefix="/matrimonio")

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

ALLOWED_PATCH_FIELDS = [
    "fecha_registro_mat",
    "lugar_registro_mat",
    "fecha_matrimonio",
    "lugar_matrimonio",
    "hora_matrimonio",
]


MODEL_FIELDS_ORDER = matrimonio_model.TODOS_LOS_CAMPOS[1:]

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
                        "error": "Faltan campos obligatorios para la creación.",
                        "campos_faltantes": missing_fields,
                    }
                ),
                400,
            )
            
        try:
            matrimonio_model.crear_matrimonio_db(
                data["numero_folio"],
                data["numero_tomo"],
                data["fecha_registro_mat"],
                data["lugar_registro_mat"],
                data["id_empleado"],
                data["fecha_matrimonio"],
                data["lugar_matrimonio"],
                data["hora_matrimonio"],
                data["id_ciudadanoC1"],
                data["id_ciudadanoC2"],
                data["id_ciudadanoMC1"],
                data["id_ciudadanoPC1"],
                data["id_ciudadanoMC2"],
                data["id_ciudadanoPC2"],
                data["id_ciudadanoMT1"],
                data["id_ciudadanoMT2"],
            )
            return jsonify({"message": "Acta de matrimonio creada."}), 201

        except IntegrityError as e:
            return (
                jsonify(
                    {
                        "error": "Error: El número de folio o tomo ya existe.",
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
        
        if not matrimonio:
            return jsonify({"error": f"Acta de Matrimonio {acta_matrimonio} no encontrada."}), 404

        return jsonify(matrimonio), 200


    @matrimonio_bp.route("/<int:acta_matrimonio>", methods=["PATCH"])
    def actualizar_acta_parcial(acta_matrimonio):
        
        data = request.get_json()

        if not data:
            return (
                jsonify({"Error": "No se recibieron datos JSON para actualizar."}),
                400,
            )

        matrimonio_actual = matrimonio_model.obtener_matrimonio_por_acta(acta_matrimonio)

        if not matrimonio_actual:
            return (
                jsonify({"Error": f"Acta de Matrimonio {acta_matrimonio} no encontrada."}),
                404,
            )

        valores_a_actualizar = dict(matrimonio_actual)
        
        for key, value in data.items():
            if key in ALLOWED_PATCH_FIELDS: 
                valores_a_actualizar[key] = value

        argumentos_para_db = [
            valores_a_actualizar.get(campo)
            for campo in MODEL_FIELDS_ORDER
        ]
        
        argumentos_para_db.append(acta_matrimonio)

        try:
            matrimonio_model.actualizar_matrimonio_db(*argumentos_para_db)

            return jsonify({"Message": f"Acta {acta_matrimonio} actualizada (PATCH) exitosamente. Solo se modificaron los campos de fecha y lugar."})
        
        except IntegrityError as e:
            return (
                jsonify(
                    {
                        "error": "Error de integridad al actualizar. Revise que los folios/tomos no se repitan.",
                        "detalle": f"Detalle DB: {e}",
                    }
                ),
                400,
            )
        except Exception as e:
            print(f"Error al actualizar matrimonio: {e}")
            return (
                jsonify({"error": "Error interno al actualizar.", "detalle_tecnico": str(e)}),
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
        
    @matrimonio_bp.route("/certificado/<int:acta_matrimonio>", methods=["GET"])
    def obtener_certificado_completo(acta_matrimonio):
       
        matrimonio = matrimonio_model.obtener_certificado_por_acta(acta_matrimonio)
        
        if not matrimonio:
            return jsonify({"error": f"Acta de Matrimonio {acta_matrimonio} no encontrada para certificado."}), 404
        
        
        try:
            import json
            for key in matrimonio:
                if key.startswith('id_ciudadano') or key == 'id_empleado':
                    if isinstance(matrimonio[key], str) and matrimonio[key].strip():
                        matrimonio[key] = json.loads(matrimonio[key])
                    elif matrimonio[key] is None:
                        matrimonio[key] = {'primer_nombre': None, 'primer_apellido': None}

        except Exception as e:
            print(f"Error deserializando JSON en la vista: {e}")
            return jsonify({"error": "Error interno al procesar los datos del certificado."}), 500


        return jsonify(matrimonio), 200