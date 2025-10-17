from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import load_encrypted_config
from pathlib import Path
from urllib.parse import quote_plus  # para tratar senhas com caracteres especiais

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '65c31d35bc79ff5e551a20326cbca1a8'

    # Configura DB
    config_file = Path(__file__).parent / 'database.ini'
    db_config = load_encrypted_config(config_file)
    pg = db_config['postgresql']
    password = quote_plus(pg['password'])
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{pg['username']}:{password}@{pg['hostname']}:{pg['port']}/{pg['database']}"
    )

    # Inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "info"

    # Importa modelos e cria tabelas
    from .models import Usuario, ConteudoTeste
    with app.app_context():
        db.create_all()

    # Callback Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Importa e registra blueprints
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')  # só registrar o blueprint

    return app