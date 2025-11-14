from flask import Blueprint
from app.vistas.nacimiento_vistas import setup_routes

nacimiento_bp = Blueprint('nacimientos', __name__)

setup_routes(nacimiento_bp)
