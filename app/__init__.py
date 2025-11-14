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

    CORS(app, origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ], supports_credentials=True)

    from app.models import ciudadano_model
    ciudadano_model.setup_db()
    
    from app.models import empleado_model
    empleado_model.setup_db()
    
    from app.models import nacimiento_model
    nacimiento_model.setup_db()
    
    from app.models import defuncion_model
    defuncion_model.setup_db()
    
    from app.controllers.ciudadano_controllers import ciudadano_bp 
    from app.controllers.empleado_controllers import empleado_bp
    from app.controllers.nacimiento_controllers import nacimiento_bp
    from app.controllers.defuncion_controllers import defuncion_bp
    
    
    app.register_blueprint(ciudadano_bp, url_prefix='/api/v1/ciudadanos')
    app.register_blueprint(empleado_bp, url_prefix='/api/v1/empleados')
    app.register_blueprint(nacimiento_bp, url_prefix='/api/v1/nacimientos')
    app.register_blueprint(defuncion_bp, url_prefix='/api/v1/defunciones')

    return app
