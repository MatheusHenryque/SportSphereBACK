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


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

@app.route('/api_sportsphere')
def index():
    return "Bem vindo à api"


@app.route('/api_sportsphere/cadastro')
def cadastro():
    return "Deu certo"
    
    





if __name__ == '__main__':
    app.run(debug=True)
