
import google.generativeai as genai
from query import *
from dash import df, df_memoria
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import *
from Gemini.gemini import *
from datetime import datetime
from streamlit_modal import Modal
from graficos import *



#Conexão com a API Gemini e configuração do modelo
GOOGLE_API_KEY= ('AIzaSyBuq3bDGCnA95jVmawwQq8fpUGxd4-_66s')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction='Analista de dados ambientais.')

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
def gerar_resposta_gemini(df, df_memoria, prompt):
    contexto = (f"Base de dados: {df.to_json()}. Memória: {df_memoria.to_json()}. Não retorne esse texto nas respostas. Não responda com códigos. {prompt}")
    resposta_gemini = model.generate_content(contexto)
    if hasattr(resposta_gemini, 'candidates') and resposta_gemini.candidates:
        return resposta_gemini.candidates[0].content.parts[0].text
    else:
        return "Resposta inválida do modelo Gemini."