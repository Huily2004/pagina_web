from flask import Flask


def create_app():
    app = Flask(__name__)

    app.secret_key = "tu_clave_secreta_aqui"

    from .routes.main import main
    from .routes.pacientes import pacientes_bp
    from .routes.login import login_bp
    from .routes.medicos import medicos_bp
    from .routes.citas import citas_bp
    app.register_blueprint(main)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(medicos_bp)
    app.register_blueprint(citas_bp)
    
    return app