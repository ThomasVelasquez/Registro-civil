from flask import request, jsonify
from app.models import defuncion_model
from sqlite3 import IntegrityError

REQUIRED_FIELDS = [
    'acta_defuncion', 
    'numero_folio', 
    'numero_tomo', 
    'fecha_registro_def', 
    'lugar_registro_def', 
    'fecha_fallecimiento', 
    'lugar_fallecimiento', 
    'hora_fallecimiento', 
    'causa_fallecimiento', 
    'forma_fallecimiento',
    'nro_certificado_defuncion',
    'fecha_expedicion_defuncion',
    'autoridad_expide_defuncion',
    'numero_mpps_autoridad_def',
    'denominacion_dependencia_salud', 
    'relacion_con_fallecido',
    'id_ciudadano',
    'id_ciudadano_declarante',
    'id_ciudadano_FM',
    'id_ciudadano_FP',
    'id_empleado'
]

def setup_routes(defuncion_bp):

    @defuncion_bp.route("", methods=["POST"]) 
    def crear_defuncion():
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
        fecha_registro_def = data.get("fecha_registro_def")
        lugar_registro_def = data.get("lugar_registro_def")
        fecha_fallecimiento = data.get("fecha_fallecimiento")
        lugar_fallecimiento = data.get("lugar_fallecimiento")
        hora_fallecimiento = data.get("hora_fallecimiento")
        causa_fallecimiento = data.get("causa_fallecimiento")
        forma_fallecimiento = data.get("forma_fallecimiento")
        nro_certificado_defuncion = data.get("nro_certificado_defuncion")
        fecha_expedicion_defuncion = data.get("fecha_expedicion_defuncion")
        autoridad_expide_defuncion = data.get("autoridad_expide_defuncion")
        numero_mpps_autoridad_def = data.get("numero_mpps_autoridad_def")
        denominacion_dependencia_salud = data.get("denominacion_dependencia_salud")
        relacion_con_fallecido = data.get("relacion_con_fallecido")
        id_ciudadano = data.get("id_ciudadano")
        id_ciudadano_declarante = data.get("id_ciudadano_declarante")
        id_ciudadano_FM = data.get("id_ciudadano_FM")
        id_ciudadano_FP = data.get("id_ciudadano_FP")
        id_empleado = data.get("id_empleado")

        try:
            defuncion_model.crear_defuncion_db( 
                numero_folio, 
                numero_tomo, 
                fecha_registro_def, 
                lugar_registro_def, 
                fecha_fallecimiento, 
                lugar_fallecimiento, 
                hora_fallecimiento, 
                causa_fallecimiento, 
                forma_fallecimiento,
                nro_certificado_defuncion,
                fecha_expedicion_defuncion,
                autoridad_expide_defuncion,
                numero_mpps_autoridad_def,
                denominacion_dependencia_salud, 
                relacion_con_fallecido,
                id_ciudadano,
                id_ciudadano_declarante,
                id_ciudadano_FM,
                id_ciudadano_FP,
                id_empleado
            )
            return jsonify({"message": "Defuncion Creada"}), 201

        except IntegrityError as e:
            return (
                jsonify(
                    {
                        "error": "Error: La defuncion ya existe",
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

