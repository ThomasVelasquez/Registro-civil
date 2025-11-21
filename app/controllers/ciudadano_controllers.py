from flask import Blueprint
from app.vistas.ciudadano_vistas import setup_routes

ciudadano_bp = Blueprint('ciudadanos', __name__)

setup_routes(ciudadano_bp)