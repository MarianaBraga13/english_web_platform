from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import load_encrypted_config
from pathlib import Path
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(ambiente="local"):
    """
    Cria e configura o app Flask.
    Parâmetro:
        ambiente (str): "local" ou "remoto"
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

    # Carrega configurações do banco
    config_file = Path(__file__).parent / 'database.ini'
    db_config = load_encrypted_config(config_file)

    if ambiente == "local":
        pg = db_config['postgresql']
    elif ambiente == "remoto":
        pg = db_config.get('postgresql_remoto')
        if not pg:
            raise ValueError("Configuração para banco remoto não encontrada!")
    else:
        raise ValueError(f"Ambiente inválido: {ambiente}")

    password = quote_plus(pg['password'])
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{pg['username']}:{password}@{pg['hostname']}:{pg['port']}/{pg['database']}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # evita warning

    # Inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "info"

    # Importa modelos **depois** de init_app
    with app.app_context():
        from .models import Usuario, ConteudoTeste, Testerespostas, Testegabarito, Testeresultado
        db.create_all()  # cria tabelas se não existirem

    # Callback Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from .models import Usuario
        return Usuario.query.get(int(user_id))

    # Importa e registra blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app