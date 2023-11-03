import requests
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt 
import psycopg2 as pg

app = Flask(__name__)
bcrypt = Bcrypt(app)

conn = pg.connect(
    host="localhost",
    user="postgres",
    password="Ml304210?",
    port="5432",
    dbname="SportSphere.bd"
)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  

    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not nome or not email or not senha:
        return jsonify({'message': 'Campos nome, email e senha são obrigatórios'}), 400

    senha_hashed = bcrypt.generate_password_hash(senha).decode('utf-8')

    cursor = conn.cursor()
    cursor.execute("INSERT INTO TB_USUARIO (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha_hashed))
    conn.commit()
    cursor.close()

    
    external_url_register = 'https://sport-sphere.vercel.app/Cadastro'
    try:
        response = requests.get(external_url_register)
        data = response.json()  
        
    except requests.exceptions.RequestException as e:
        pass

    return jsonify({'message': 'Usuário registrado com sucesso'}), 201

# Rota de login de usuário
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  

    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({'message': 'Campos email e senha são obrigatórios'}), 400

    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM TB_USUARIO WHERE email = %s", (email,))
    user_data = cursor.fetchone()
    cursor.close()

    if user_data and bcrypt.check_password_hash(user_data[0], senha):
        
        external_url_login = 'https://sport-sphere.vercel.app/Login'
        try:
            response = requests.get(external_url_login)
            data = response.json()  
            
        except requests.exceptions.RequestException as e:
            pass

        return jsonify({'message': 'Login bem-sucedido'}), 200
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401

if __name__ == '__main__':
    app.run(debug=True)
