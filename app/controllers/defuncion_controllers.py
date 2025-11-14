from flask import Blueprint
from app.vistas.defuncion_vistas import setup_routes

defuncion_bp = Blueprint('defunciones', __name__)

setup_routes(defuncion_bp)

