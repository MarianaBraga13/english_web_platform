from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from sshtunnel import SSHTunnelForwarder
from flask_login import LoginManager

from .config import db_config, ssh_config

db = SQLAlchemy()
#DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
#    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
#   db.init_app(app)

    hostname = db_config['hostname']
    port_id = db_config['port']
    database = db_config['database']
    username = db_config['username']
    pwd = db_config['password']

    jumpserver = ssh_config['jumpserver']
    ssh_user = ssh_config['ssh_user']
    ssh_key_path = ssh_config['ssh_key_path']

    tunnel = SSHTunnelForwarder(
        (jumpserver, 22),
        ssh_username=ssh_user,
        ssh_pkey=ssh_key_path,
        remote_bind_address=(hostname, port_id))

    tunnel.start()
    local_port = tunnel.local_bind_port


    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{username}:{pwd}@127.0.0.1:{local_port}/{database}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Usuario, ConteudoTeste
    
    with app.app_context():
        db.create_all()

    #Gerenciamento dos logins
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message = "To access this page, you need to be logged in."
    login_manager.login_message_category = "error"

    @login_manager.user_loader
    def load_usuario(id):
        return Usuario.query.get(int(id))

    return app 

