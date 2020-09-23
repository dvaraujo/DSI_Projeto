from application import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)
    criado_em = db.Column(db.DATETIME, default=datetime.now(), nullable=True)

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha, method='sha256')

    def verifica_senha(self, senha):
        return check_password_hash(self.senha, senha)

class Escritorio(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    razao_social = db.Column(db.String(250), nullable=False, unique=True)
    cnpj = db.Column(db.String(14), nullable=False, unique=True)
    n_oab = db.Column(db.String(8), nullable=False, unique=True)   
    email = db.Column(db.String(50), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)
    criado_em = db.Column(db.DATETIME, default=datetime.now(), nullable=True)

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha, method='sha256')

    def verifica_senha(self, senha):
        return check_password_hash(self.senha, senha)

class Caso(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(250), nullable=False, unique=False)
    cpf = db.Column(db.String(11), nullable=False, unique=False) 
    descricao = db.Column(db.String(1000), nullable=False, unique=False)