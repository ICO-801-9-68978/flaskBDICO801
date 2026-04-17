from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
from models import db
import forms

# Importación de los Blueprints
from alumnos.routes import alumnos_bp
from maestros.routes import maestros_bp
from cursos.routes import cursos_bp
from inscripciones.routes import inscripciones_bp
from consultas.routes import consultas_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Inicialización de extensiones
db.init_app(app)
csrf = CSRFProtect()
migrate = Migrate(app, db)

# Registro de todos los Blueprints
app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(inscripciones_bp)
app.register_blueprint(consultas_bp)

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()