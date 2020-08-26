from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Bibliotecas acessíveis globalmente
db = SQLAlchemy()


def create_app():
    """Inicia a aplicação principal"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Inicializa os plugins
    db.init_app(app)

    with app.app_context():
        # Inclui as rotas
        from . import routes

        # Registra as  Blueprints
        # app.register_blueprint(auth.auth_bp)
        # app.register_blueprint(admin.admin_bp)

        return app
