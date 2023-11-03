from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import psycopg2 as pg

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Defina uma chave secreta para flash messages
bcrypt = Bcrypt(app)

# Configuração do banco de dados
conn = pg.connect(
    host="localhost",
    user="postgres",
    password="Ml304210?",
    port="5432",
    dbname="SportSphere.bd"
)

# Rota de registro de usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if not nome or not email or not senha:
            flash('Campos nome, email e senha são obrigatórios', 'error')
        else:
            senha_hashed = bcrypt.generate_password_hash(senha).decode('utf-8')

            cursor = conn.cursor()
            cursor.execute("INSERT INTO TB_USUARIO (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha_hashed))
            conn.commit()
            cursor.close()

            flash('Usuário registrado com sucesso', 'success')
            return redirect(url_for('register'))

    return render_template('register.html')

# Rota de login de usuário
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cursor = conn.cursor()
        cursor.execute("SELECT senha FROM TB_USUARIO WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data and bcrypt.check_password_hash(user_data[0], senha):
            flash('Login bem-sucedido', 'success')
            return redirect(url_for('login'))
        else:
            flash('Credenciais inválidas', 'error')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
