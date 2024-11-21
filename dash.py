import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import *
from Gemini.gemini import *
from datetime import datetime
from streamlit_modal import Modal
from graficos import *

st.set_page_config(
    page_title="Dashboard",  # título da página
    page_icon=":lizard:",  # ícone da página (opcional)
    layout="wide",  # ou "wide", se preferir layout mais amplo
    initial_sidebar_state='expanded')

# Consultas iniciais nas duas tabelas do banco
query = """
    SELECT * 
    FROM tb_registro
    WHERE regiao IS NOT NULL 
"""
memoria = ("SELECT * FROM tb_memoria")

df = conexao(query)
df_memoria = conexao(memoria)

df['tempo_registro'] = pd.to_datetime(df['tempo_registro'])

df_selecionado = df.copy()   # Cria uma copia do df original.:

# ****************************** MENU LATERAL ******************************

st.sidebar.image("images/logo.png", use_container_width=True)

st.sidebar.markdown(f'<h1 style="text-transform: uppercase;">{'Selecione a região para gerar o gráfico'}</h1>', unsafe_allow_html=True)  

st.sidebar.subheader("Região")
SP = st.sidebar.checkbox("São Paulo", value=True)
ABC = st.sidebar.checkbox("Grade ABC", value=True)

if SP == False and ABC == False:
    st.sidebar.markdown(f'<p style="font-size:16px;font-weight:bold;background-color:#D3D4CD;display:flex;justify-content:center;padding:10px;border-radius:10px;">{"SELECIONE UMA REGIÃO!"}<p>', unsafe_allow_html=True)
    #st.sidebar.warning("Selecione uma região!")

# Lista de regiões selecionadas
regioes_selecionadas = []
if SP:
    regioes_selecionadas.append("São Paulo")
if ABC:
    regioes_selecionadas.append("Grande ABC")

# Filtrando o DataFrame com base nas regiões selecionadas
if regioes_selecionadas:
    df = df[df["regiao"].isin(regioes_selecionadas)]

def aplicar_filtros(df):
    # Filtro por intervalo de tempo
    if "tempo_registro" in df.columns:
        # Datas mínimas e máximas
        min_data = df["tempo_registro"].min()
        max_data = df["tempo_registro"].max()

        # Campos de data no menu lateral
        data_inicio = st.sidebar.date_input(
            "Data de Início", 
            min_data.date(), 
            min_value=min_data.date(), 
            max_value=max_data.date()
        )
        data_fim = st.sidebar.date_input(
            "Data de Fim", 
            max_data.date(), 
            min_value=min_data.date(), 
            max_value=max_data.date()
        )

        # Converter as datas selecionadas para datetime
        tempo_registro_range = (
            pd.to_datetime(data_inicio),
            pd.to_datetime(data_fim) + pd.DateOffset(days=1) - pd.Timedelta(seconds=1)
        )

        # Filtrar o DataFrame pelo intervalo de tempo
        df = df[
            (df["tempo_registro"] >= tempo_registro_range[0]) &
            (df["tempo_registro"] <= tempo_registro_range[1])
        ]

    # Retorna o DataFrame filtrado
    return df

# **************************** HOME****************************
def Home():
  
    # Título principal
    st.title("Dashboard de Monitoramento")

# ---------------------- APLICAÇÃO GEMINI -----------------------------------------------

    # Configuração do modal
    modal = Modal(
        "Análise Inteligente",
        key="gemini-modal",
        padding=40,
        max_width=744
    )

    # Botão para abrir o modal
    open_modal = st.button("Análise inteligente", icon='🤖', key="Analise")
    if open_modal:
        modal.open()

    # Configuração do conteúdo do modal
    if modal.is_open():
        with modal.container():
            st.write("Digite sua pergunta sobre a base de dados")
            user_input = st.text_area("Escreva algo aqui...", "")

            # Geração de conteúdo ao clicar em "Enviar"
            if st.button("Gerar análise"):
                if user_input.strip():
                    try:
                        
                        prompt = user_input
                        
                        resposta_gemini = gerar_resposta_gemini(df, df_memoria, prompt)
                        
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

    # Linha visível de delimitação
    st.markdown(
        """
        <hr style="
            border: none; 
            border-top: 2px solid #3E5050; /* Define a cor da linha */
            margin-top: 10px;             /* Espaçamento acima da linha */
            margin-bottom: 20px;          /* Espaçamento abaixo da linha */
        ">
        """,
        unsafe_allow_html=True
    )   

# ****************************MEDIAS****************************

    # Verifique se o DataFrame selecionado não está vazio
    if df_selecionado.empty:
        st.warning("Nenhum dado disponível para calcular as médias.")

    # Cálculo das médias
    media_umidade = df_selecionado["umidade"].mean()
    media_temperatura = df_selecionado["temperatura"].mean()
    media_co2 = df_selecionado["co2"].mean()

    # Layout em colunas para exibir as métricas
    col1, col2, col3 = st.columns(3)

    # Estilo personalizado para as caixas
    caixa_estilo = """
    <div style="
        background-color: #D3D4CD;
        border-radius: 10px;
        padding: 5px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        text-align: center;
    ">
        <h3 style="color: #215132; margin-bottom: 10px;">{titulo}</h3>
        <p style="font-size: 23px; font-weight: bold; margin: 0;">{valor}</p>
    </div>
    """

    # Exibição das caixas em cada coluna
    with col1:
        st.markdown(
            caixa_estilo.format(
                titulo="Média de Umidade", valor=f"{media_umidade:.2f}%"
            ),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            caixa_estilo.format(
                titulo="Média de Temperatura", valor=f"{media_temperatura:.2f}°C"
            ),
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            caixa_estilo.format(
                titulo="Média de CO2", valor=f"{media_co2:.2f} ppm"
            ),
            unsafe_allow_html=True,
        )
        
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# **************************** PLOTANDO GRÁFICOS ****************************
def graficos(df):
    
    # Verifica se há dados no DataFrame
    if df.empty:
        st.warning("Nenhum dado disponível para os filtros aplicados.")
        return

    # Plotagem dos gráficos
    col1, space, col2 = st.columns([10, 5, 10])

    with col1:
        grafico_barras(df)
        grafico_linhas(df)

    with col2:
        grafico_dispersao(df)
        grafico_area(df)

    grafico_barras_empilhadas(df)

# **************************** CHAMANDO A FUNÇÃO ****************************

df_filtrado = aplicar_filtros(df)

Home()
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados!")
else:
    graficos(df_filtrado)
    rodape_html = """
    <style>
    footer {
        position: relative; /* Permite que o rodapé seja colocado após o conteúdo */
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px 0;
        font-size: 14px;
        color: #333;
        
    }
    </style>
    <footer>
        <p>Copyright © 2024 - Todos os direitos reservados - Equipe Lagartixa</p>
    </footer>
    """
    st.markdown(rodape_html, unsafe_allow_html=True)