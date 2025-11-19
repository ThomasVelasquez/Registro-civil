from flask import Blueprint
from app.vistas.divorcio_vistas import setup_routes

divorcio_bp = Blueprint("divorcios", __name__)

setup_routes(divorcio_bp)
