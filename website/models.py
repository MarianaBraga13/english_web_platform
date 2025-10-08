from . import db 
from flask_login import UserMixin
from dataclasses import dataclass
from sqlalchemy.sql import func

#User Mixin permite o uso de imports da lib flask_login!

class Usuario(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    senha = db.Column(db.String(255))
    nivel_usuario = db.Column(db.String(1))

    def get_id(self):
        return (self.user_id)

@dataclass
class ConteudoTeste(db.Model):
    id:int = db.Column(db.Integer, primary_key = True)
    titulo: str = db.Column(db.String(150))
    descricao: str = db.Column(db.String(1000))
    url: str = db.Column(db.String(500))
    nivel_conteudo: str = db.Column(db.String(1))

class Testerespostas(db.Model):
    test_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    name_test = db.Column(db.String(50), nullable = False)
    insert_at = db.Column(db.DateTime(timezone=True), default=func.now())
    question_1 = db.Column(db.String(1))
    question_2 = db.Column(db.String(1))
    question_3 = db.Column(db.String(1))
    question_4 = db.Column(db.String(1))
    question_5 = db.Column(db.String(1))
    question_6 = db.Column(db.String(1))
    question_7 = db.Column(db.String(1))
    question_8 = db.Column(db.String(1))
    question_9 = db.Column(db.String(1))
    question_10 = db.Column(db.String(1))
    question_11 = db.Column(db.String(1))
    question_12 = db.Column(db.String(1))
    question_13 = db.Column(db.String(1))
    question_14 = db.Column(db.String(1))
    question_15 = db.Column(db.String(1))

class Testegabarito(db.Model):
    test_id = db.Column(db.Integer, primary_key = True)
    name_test = db.Column(db.String(50), unique= True, nullable = False)
    question_1 = db.Column(db.String(1))
    question_2 = db.Column(db.String(1))
    question_3 = db.Column(db.String(1))
    question_4 = db.Column(db.String(1))
    question_5 = db.Column(db.String(1))
    question_6 = db.Column(db.String(1))
    question_7 = db.Column(db.String(1))
    question_8 = db.Column(db.String(1))
    question_9 = db.Column(db.String(1))
    question_10 = db.Column(db.String(1))
    question_11 = db.Column(db.String(1))
    question_12 = db.Column(db.String(1))
    question_13 = db.Column(db.String(1))
    question_14 = db.Column(db.String(1))
    question_15 = db.Column(db.String(1))

class Testeresultado(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    name_test = db.Column(db.String(50), nullable = False)
    insert_at = db.Column(db.DateTime(timezone=True), default=func.now())
    percet_result = db.Column(db.Float, nullable = False)
    question_1 = db.Column(db.String(1))
    question_2 = db.Column(db.String(1))
    question_3 = db.Column(db.String(1))
    question_4 = db.Column(db.String(1))
    question_5 = db.Column(db.String(1))
    question_6 = db.Column(db.String(1))
    question_7 = db.Column(db.String(1))
    question_8 = db.Column(db.String(1))
    question_9 = db.Column(db.String(1))
    question_10 = db.Column(db.String(1))
    question_11 = db.Column(db.String(1))
    question_12 = db.Column(db.String(1))
    question_13 = db.Column(db.String(1))
    question_14 = db.Column(db.String(1))
    question_15 = db.Column(db.String(1))