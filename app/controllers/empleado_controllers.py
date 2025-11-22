from flask import Blueprint
from app.vistas.empleado_vistas import setup_routes

empleado_bp = Blueprint('empleados', __name__)

setup_routes(empleado_bp)