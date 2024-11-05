# pip install mysql-connector-python
# pip install streamlit

import mysql.connector
import pandas as pd
from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import google.generativeai as genai

# ********************** CONEXÃO COM O BANCO DE DADOS **********************

app = Flask("registro")     # Nome do aplicativo.

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # Configura o SQLAlchemy para rastrear modificações. 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/bd_medidor'

mybd = SQLAlchemy(app)      # Cria uma instância do SQLAlchemy, passando a aplicação Flask como parâmetro. 

# -------------------INICIO DA APLICAÇÃO GEMINI---------------------------------------------

#Conexão com a API Gemini e configuração do modelo
GOOGLE_API_KEY= ('AIzaSyBuq3bDGCnA95jVmawwQq8fpUGxd4-_66s')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction='Assistente de dados ambientais com acesso a histórico de temperatura, umidade, CO₂, pressão, altitude, poeira e região.')


# Classe da tabela memória
class TbMemoria(mybd.Model):
    __tablename__ = 'tb_memoria'
    id = mybd.Column(mybd.Integer, primary_key=True)
    prompt = mybd.Column(mybd.Text, nullable=False)
    resposta_gemini = mybd.Column(mybd.Text, nullable=False)
    
# Função para salvar na memória
def save_to_memory(prompt, resposta_gemini):
    with app.app_context():
        new_entry = TbMemoria(prompt=prompt, resposta_gemini=resposta_gemini)
        mybd.session.add(new_entry)
        mybd.session.commit()

# Função para interagir com o Gemini
def gerar_resposta_gemini(df, memoria, prompt):
    contexto = (f"Base de dados: {df.to_json()}. Memória: {memoria.to_json()}. Não retorne esse texto nas respostas. Não responda com códigos. {prompt}")
    resposta_gemini = model.generate_content(contexto)
    if hasattr(resposta_gemini, 'candidates') and resposta_gemini.candidates:
        return resposta_gemini.candidates[0].content.parts[0].text
    else:
        return "Resposta inválida do modelo Gemini."
        
#--------------------------------------------------------------------

def conexao(query):
    conn = mysql.connector.connect(
        host ='127.0.0.1',
        port='3306',
        user='root',
        password='senai@134',
        db='bd_medidor'
              
    )
    
    dataframe = pd.read_sql(query, conn)
    
    conn.close()
    
    return dataframe