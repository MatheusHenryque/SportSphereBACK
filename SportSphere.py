from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt 
from sqlalchemy import create_engine, Column, String, Integer, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests

app = Flask(__name__)
bcrypt = Bcrypt(app)


engine = create_engine('sqlite:///sport.db')


Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'TB_USUARIO'
    id = Column(Integer, primary_key=True)
    nome = Column(String(60))
    senha = Column(String(60))

class Cadastro(Base):
    __tablename__ = 'TB_CADASTRO'
    id_usuario = Column(Integer, primary_key=True)
    nome_usuario = Column(String(60))
    email = Column(String(100))
    telefone = Column(Integer)
    senha_usuario = Column(String(60))

# Criar a tabela no banco de dados
Base.metadata.create_all(engine)

# Criar uma instância da sessão
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/', methods=['POST'])
def login():
    data = request.get_json()  
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({'message': 'Campos email e senha são obrigatórios'}), 400

    # Consultar o banco de dados usando SQLAlchemy
    usuario = session.query(Usuario).filter_by(email=email).first()

    if usuario and bcrypt.check_password_hash(usuario.senha, senha):
        external_url_login = 'https://sport-sphere.vercel.app'
        try:
            response = requests.get(external_url_login)
            data = response.json()  
        except requests.exceptions.RequestException as e:
            pass

        return jsonify({'message': 'Login bem-sucedido'}), 200
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401   

@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()  

    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not nome or not email or not senha:
        return jsonify({'message': 'Campos nome, email e senha são obrigatórios'}), 400

    # Gerar o hash da senha
    senha_hashed = bcrypt.generate_password_hash(senha).decode('utf-8')

    # Adicionar usuário ao banco de dados usando SQLAlchemy
    novo_usuario = Cadastro(nome_usuario=nome, email=email, senha_usuario=senha_hashed)
    session.add(novo_usuario)
    session.commit()

    external_url_register = 'https://sport-sphere.vercel.app/Cadastro'
    try:
        response = requests.get(external_url_register)
        data = response.json()  
    except requests.exceptions.RequestException as e:
        pass

    return jsonify({'message': 'Usuário registrado com sucesso'}), 201

if __name__ == '__main__':
    app.run(debug=True)
