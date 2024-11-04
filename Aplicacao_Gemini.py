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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:525748@127.0.0.1/bd_medidor' #A senha está diferente

mybd = SQLAlchemy(app)   
   

def conexao(query):
    with app.app_context():  
        result = mybd.session.execute(text(query))  
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df
    
# -------------------INICIO DA APLICAÇÃO GEMINI---------------------------------------------

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
def gerar_resposta_gemini(prompt):
    contexto = (f"Base de dados: {df.to_json()}. Memória: {df_memoria.to_json}. Não retorne esse texto nas respostas. Não responda com códigos. {prompt}")
    resposta_gemini = model.generate_content(contexto)
    if hasattr(resposta_gemini, 'candidates') and resposta_gemini.candidates:
        return resposta_gemini.candidates[0].content.parts[0].text
    else:
        return "Resposta inválida do modelo Gemini."    
#--------------------------------------------------------------------

#Conexão com a API Gemini e configuração do modelo
GOOGLE_API_KEY= ('AIzaSyBuq3bDGCnA95jVmawwQq8fpUGxd4-_66s')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction='Assistente de dados ambientais com acesso a histórico de temperatura, umidade, CO₂, pressão, altitude, poeira e região.')

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
                    
                    prompt = user_input
                    
                    resposta_gemini = gerar_resposta_gemini(prompt)
        
                    st.write("Resposta da análise:")
                    st.write(resposta_gemini) 
                              
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
            
# -------------------FIM DA APLICAÇÃO GEMINI ---------------------------------------------