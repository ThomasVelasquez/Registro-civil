from flask import Flask
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
    app.config['DATABASE_PATH'] = os.getenv('DATABASE_PATH')

    # Permitir tus orígenes de dev (http + 127.0.0.1)
    CORS(app, origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ], supports_credentials=True)

    from app.models import ciudadano_model
    ciudadano_model.setup_db()

    from app.controllers.ciudadano_controllers import ciudadano_bp
    # Registrar blueprint — si tus rutas dentro del blueprint usan '' o '/', controla las barras
    app.register_blueprint(ciudadano_bp, url_prefix='/api/v1/ciudadanos')

    return app
