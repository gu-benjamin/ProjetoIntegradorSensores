
import google.generativeai as genai
from query import *
from dash import df
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
GOOGLE_API_KEY= ('AIzaSyArDlZQJbEUquhe1XBa59_ImBpnMwgGpgw')
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

# # Função para interagir com o Gemini
# def gerar_resposta_gemini(df, df_memoria, prompt):
#     contexto = (f"Base de dados: {df.to_json()}. Memória: {df_memoria.to_json()}. Não retorne esse texto nas respostas. Não responda com códigos. {prompt}")
#     resposta_gemini = model.generate_content(contexto)
#     if hasattr(resposta_gemini, 'candidates') and resposta_gemini.candidates:
#         return resposta_gemini.candidates[0].content.parts[0].text
#     else:
#         return "Resposta inválida do modelo Gemini."


def gerar_resposta_gemini(df_gemini, df_memoria, df_poluentes, prompt):
    # Reduz os dados para evitar contextos extensos
    resumo_df = df.head(500).to_json()  # Resumo da tabela principal
    resumo_memoria = df_memoria.head(20).to_json()  # Resumo da memória
    resumo_poluentes = df_poluentes.to_json()  # Resumo dos dados de poluentes

    # Monta o contexto do prompt
    contexto = (
        f"Base de dados: {resumo_df}. "
        f"Memória: {resumo_memoria}. "
        f"Dados de poluentes: {resumo_poluentes}. "
        f"Não retorne esse texto nas respostas. Não responda com códigos. {prompt}"
    )
    
    # Gera a resposta usando o modelo Gemini
    resposta_gemini = model.generate_content(contexto)
    if hasattr(resposta_gemini, 'candidates') and resposta_gemini.candidates:
        resposta_final = resposta_gemini.candidates[0].content.parts[0].text

        # Salva no banco de dados
        save_to_memory(prompt, resposta_final)
        
        return resposta_final
    else:
        return "Resposta inválida do modelo Gemini."
