from flask import Blueprint, jsonify, request
import app.models.reporte_model as reporte_model


reporte_bp = Blueprint("reporte_bp", __name__) 


@reporte_bp.route("/volumen", methods=["GET"])
def volumen_total():
    try:
        data = reporte_model.get_volumen_total()
        return jsonify({
            "message": "Volumen total de actas por tipo.",
            "data": data
        }), 200
    except Exception as e:
        print(f"Error en volumen_total: {e}")
        return jsonify({"error": "Error interno del servidor al obtener volumen."}), 500


@reporte_bp.route("/anual", methods=["GET"])
def reporte_anual():
    anio = request.args.get("anio")
    
    if not anio:
        return jsonify({"error": "Parámetro 'anio' es requerido."}), 400
    
    if not anio.isdigit() or len(anio) != 4:
        return jsonify({"error": "Formato de año inválido. Use YYYY."}), 400

    try:
        data = reporte_model.get_registros_por_anio(anio)
        return jsonify({
            "message": f"Reporte de actas registradas en el año {anio}.",
            "data": data
        }), 200
    except Exception as e:
        print(f"Error en reporte_anual: {e}")
        return jsonify({"error": "Error interno del servidor al obtener reporte anual."}), 500


@reporte_bp.route("/top-empleados", methods=["GET"])
def top_empleados():
    try:
        data = reporte_model.get_top_empleados_nacimiento()
        return jsonify({
            "message": "Top 5 empleados con más registros de Nacimiento.",
            "data": data
        }), 200
    except Exception as e:
        print(f"Error en top_empleados: {e}")
        return jsonify({"error": "Error interno del servidor al obtener top empleados."}), 500