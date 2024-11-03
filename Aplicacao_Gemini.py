import numpy as np
import streamlit as st
import pandas as pd
from query import *
from datetime import datetime
from streamlit_modal import Modal
import google.generativeai as genai
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import text

app = Flask("registro") 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:525748@127.0.0.1/bd_medidor'

mybd = SQLAlchemy(app)   
   

def conexao(query):
    with app.app_context():  
        result = mybd.session.execute(text(query))  
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df

# ------- Definição da classe para tb_memoria - Inserir na Main ------

class TbMemoria(mybd.Model):
    __tablename__ = 'tb_memoria'
    id = mybd.Column(mybd.Integer, primary_key=True)
    prompt = mybd.Column(mybd.String(255), nullable=False)
    resposta_gemini = mybd.Column(mybd.Text, nullable=False)
    
# Função para salvar na memória
def save_to_memory(prompt, resposta_gemini):
    with app.app_context():
        new_entry = TbMemoria(prompt=prompt, resposta_gemini=resposta_gemini)
        mybd.session.add(new_entry)
        mybd.session.commit()
#--------------------------------------------------------------------

#Conexão com a API Gemini
GOOGLE_API_KEY= ('AIzaSyBuq3bDGCnA95jVmawwQq8fpUGxd4-_66s')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Consultas iniciais nas duas tabelas do banco
query = "SELECT * FROM tb_registro"
memoria = ("SELECT * FROM tb_memoria")

df = conexao(query)
df_memoria = conexao(memoria)
df['tempo_registro'] = pd.to_datetime(df['tempo_registro'])  # Converte para datetime
        
# Configuração do modal
modal = Modal(
    "Análise Inteligente",
    key="gemini-modal",
    padding=40,
    max_width=744
)

# Botão para abrir o modal
open_modal = st.button("Análise inteligente", icon='🤖')
if open_modal:
    modal.open()

# Configuração do conteúdo do modal
if modal.is_open():
    with modal.container():
        st.write("Digite sua pergunta sobre a base de dados...")
        user_input = st.text_area("Escreva algo aqui...", "")

        # Geração de conteúdo ao clicar em "Enviar"
        if st.button("Gerar análise"):
            if user_input.strip():
                try:
                    contexto = (f"Base de dados: {df.to_json()}. Memória: {df_memoria.to_json}. Não retorne esse texto nas respostas. Não responda com códigos")
                    
                    prompt = (f"{contexto} Responda: {user_input}")
                    
                    resposta_gemini = model.generate_content(prompt)
                    
                    #Transforma a resposta em text
                    if hasattr(resposta_gemini, 'text'):
                        st.write("Resposta da análise:")
                        st.write(resposta_gemini.text)
                              
                    # Armazena o novo prompt e resposta na memória
                    save_to_memory(prompt, resposta_gemini)

                    print("Resposta gerada pelo Gemini:")
                    print(resposta_gemini)
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro ao acessar gerar resposta: {e}")
            else:
                st.warning("Por favor, insira uma pergunta válida.")
        
        if st.button('Fechar'):
            modal.close()