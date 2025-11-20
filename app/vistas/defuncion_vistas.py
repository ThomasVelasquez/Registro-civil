from flask import request, jsonify
from app.models import defuncion_model
from sqlite3 import IntegrityError

REQUIRED_FIELDS = [
    'acta_defuncion',
    'numero_folio',
    'numero_tomo',
    'fecha_registro_def',
    'lugar_registro_def',
    'id_empleado',
    'id_ciudadano',
    'fecha_fallecimiento',
    'lugar_fallecimiento',
    'hora_fallecimiento',
    'causa',
    'forma',
    'nro_certificado_def',
    'fecha_expedicion_def',
    'autoridad_expide_def',
    'numero_mpps_autoridad_def',
    'denominacion_dependencia_salud',
    'id_ciudadano_declarante',
    'relacion_con_fallecido',
    'id_ciudadanoC',
    'id_ciudadano_FM',
    'id_ciudadano_FP'
]

def setup_routes(defuncion_bp):

    @defuncion_bp.route("", methods=["POST"]) 
    def crear_defuncion():
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

        numero_folio = data.get("numero_folio")
        numero_tomo = data.get("numero_tomo")
        fecha_registro_def = data.get("fecha_registro_def")
        lugar_registro_def = data.get("lugar_registro_def")
        id_empleado = data.get("id_empleado")
        id_ciudadano = data.get("id_ciudadano")
        fecha_fallecimiento = data.get("fecha_fallecimiento")
        lugar_fallecimiento = data.get("lugar_fallecimiento")
        hora_fallecimiento = data.get("hora_fallecimiento")
        causa = data.get("causa")
        forma = data.get("forma")
        nro_certificado_def = data.get("nro_certificado_def")
        fecha_expedicion_def = data.get("fecha_expedicion_def")
        autoridad_expide_def = data.get("autoridad_expide_def")
        numero_mpps_autoridad_def = data.get("numero_mpps_autoridad_def")
        denominacion_dependencia_salud = data.get("denominacion_dependencia_salud")
        id_ciudadano_declarante = data.get("id_ciudadano_declarante")
        relacion_con_fallecido = data.get("relacion_con_fallecido")
        id_ciudadanoC = data.get("id_ciudadanoC")
        id_ciudadano_FM = data.get("id_ciudadano_FM")
        id_ciudadano_FP = data.get("id_ciudadano_FP")

        try:
            defuncion_model.crear_defuncion_db( 
                numero_folio,
                numero_tomo,
                fecha_registro_def,
                lugar_registro_def,
                id_empleado,
                id_ciudadano,
                fecha_fallecimiento,
                lugar_fallecimiento,
                hora_fallecimiento,
                causa,
                forma,
                nro_certificado_def,
                fecha_expedicion_def,
                autoridad_expide_def,
                numero_mpps_autoridad_def,
                denominacion_dependencia_salud,
                id_ciudadano_declarante,
                relacion_con_fallecido,
                id_ciudadanoC,
                id_ciudadano_FM,
                id_ciudadano_FP
            )
            return jsonify({"message": "Defunción Creada."}), 201

        except IntegrityError as e:
            return (
                jsonify(
                    {
                        "error": "Error: La acta de defunción ya existe.",
                        "detalle": f"Detalle DB: {e}",
                    }
                ),
                400,
            )

        except Exception as e:
            print(f"Error inesperado: {e}")
            return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500
        
    @defuncion_bp.route("/", methods=["GET"])
    def listar_defunciones():
        defunciones = defuncion_model.obtener_todas_defunciones()
        return jsonify(defunciones), 200

