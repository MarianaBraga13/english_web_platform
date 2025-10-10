from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from sshtunnel import SSHTunnelForwarder
from .config import db_config, ssh_config

db = SQLAlchemy()

def create_app(ambiente="local"):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'

    if ambiente == "local":
        #Banco local
        username = db_config['username']
        password = db_config['password']
        database = db_config['database']
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@localhost:5432/{database}'
        print("Conectando ao banco de dados LOCAL...")

    elif ambiente == "remoto":
        #Banco via túnel SSH
        hostname = db_config['hostname']
        port_id = db_config['port']
        database = db_config['database']
        username = db_config['username']
        pwd = db_config['password']

        #jumpserver para conectar com o servidor remoto (AWS)
        jumpserver = ssh_config['jumpserver']
        ssh_user = ssh_config['ssh_user']
        ssh_key_path = ssh_config['ssh_key_path']

        try:
            tunnel = SSHTunnelForwarder(
                (jumpserver, 22),
                ssh_username=ssh_user,
                ssh_pkey=ssh_key_path,
                remote_bind_address=(hostname, port_id)
            )
            tunnel.start()
            local_port = tunnel.local_bind_port

            app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{username}:{pwd}@127.0.0.1:{local_port}/{database}'
            print(f"Conectado ao banco REMOTO via túnel SSH (porta local{local_port})")
        
        except Exception as e:
            print("Falha ao conectar via túnel SSH", e)
    else:
        raise ValueError("Ambiente inválido. Use 'local' ou 'remoto'.")

    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Usuario, ConteudoTeste
    with app.app_context():
        db.create_all()

    #Login Manager (para acessar a página é necessário fazer o login)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message = "To access this page you need to be logged in."
    login_manager.login_message_category = "error"

    #acrescentando o decorator para condicionar o meio de reconhecimento do user: seu id
    @login_manager.user_loader
    def load_usuario(id):
        return Usuario.query.get(int(id))
    
    return app





