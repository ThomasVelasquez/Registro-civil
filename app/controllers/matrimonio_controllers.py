from flask import Blueprint
from app.vistas.matrimonio_vistas import setup_routes

matrimonio_bp = Blueprint("matrimonios", __name__)

setup_routes(matrimonio_bp)
