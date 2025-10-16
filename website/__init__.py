from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import load_encrypted_config
from pathlib import Path

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '65c31d35bc79ff5e551a20326cbca1a8'  # ou usa a do .env se preferir

    # Carrega o banco
    config_file = Path(__file__).parent / 'database.ini'
    db_config = load_encrypted_config(config_file)

    # Escolhe local ou remoto conforme desejar
    pg = db_config['postgresql']

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{pg['username']}:{pg['password']}@"
        f"{pg['hostname']}:{pg['port']}/{pg['database']}"
    )


    db.init_app(app)
    return app