from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Bibliotecas acessíveis globalmente
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    """Inicia a aplicação principal"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Inicializa os plugins
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Inclui as rotas
        from . import routes, models

        # Registra as  Blueprints
        # app.register_blueprint(auth.auth_bp)
        # app.register_blueprint(admin.admin_bp)

        return app
