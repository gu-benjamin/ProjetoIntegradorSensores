import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import *
from datetime import datetime
from streamlit_modal import Modal

def grafico_barras(df_selecionado):
    
    with st.expander("Selecione os eixos"): 
        colunaX = st.selectbox(
            "Eixo X",
            options = ["umidade", "temperatura", "pressao", "altitude", "co2", "poeira"],
            index = 0,
            key='eixox1'
        )
        
        colunaY = st.selectbox(
            "Eixo Y",
            options = ["umidade", "temperatura", "pressao", "altitude", "co2", "poeira"],
            index = 1,
            key='eixoy1'
        )
    
    if colunaX == colunaY:
        st.warning("Selecione uma opção diferente para os eixos X e Y")
        return
    
    try:
        cores_personalizadas = {'São Paulo': '#455354', 'Grande ABC': '#77A074'}           
        fig_valores = px.bar(
            df_selecionado,      
            x = colunaX,        
            y = colunaY,
            color = "regiao",
            orientation = "v",  
            title = f"Gráfico de Barras por Região: {colunaX.capitalize()} vs {colunaY.capitalize()}",
            color_discrete_map = cores_personalizadas,        
            template = "plotly_white"
            )
        
    except Exception as e:
        st.error(f"Erro ao criar gráfico de barras:  {e}")
    st.plotly_chart(fig_valores, use_container_width=True)
    
def grafico_linhas(df_selecionado):
    # Seleção da coluna X  |  selectbox ==> Cria uma caixa de seleção na barra lateral. 
   
    with st.expander("Selecione os eixos"):
        colunaX = st.selectbox(
            "Eixo X",
            options = ["tempo_registro"],
            index = 0,
            key='eixox2'
        )

        # Seleção da coluna Y  |  selectbox ==> Cria uma caixa de seleção na barra lateral. 
        colunaY = st.selectbox(
            "Eixo Y",
            options = ["umidade", "temperatura", "pressao", "co2", "poeira"],
            index = 1,
            key='eixoy2'
        )
    
    if colunaX == colunaY:
        st.warning("Selecione uma opção diferente para os eixos X e Y")
        return
    
    try: 
        cores_personalizadas = {'São Paulo': '#455354', 'Grande ABC': '#77A074'}          
        fig_valores2 = px.line(
            df_selecionado,
            x=colunaX,
            y=colunaY,
            color="regiao",
            title=f"Gráfico de Linhas: {colunaX.capitalize()} vs {colunaY.capitalize()}",
            color_discrete_map=cores_personalizadas,
            line_shape='linear', 
            markers=True  # Para mostrar marcadores nos pontos
        )   
        
    except Exception as e:
        st.error(f"Erro ao criar gráfico de barras:  {e}")
    st.plotly_chart(fig_valores2, use_container_width=True)
    
def grafico_dispersao(df_selecionado):
    # Seleção da coluna X  |  selectbox ==> Cria uma caixa de seleção na barra lateral. 
    with st.expander("Selecione os eixos"):    
        colunaX = st.selectbox(
            "Eixo X",
            options = ["umidade", "temperatura", "pressao", "altitude", "co2", "poeira", "tempo_registro"],
            index = 0,
            key='eixox3'
        )

        # Seleção da coluna Y  |  selectbox ==> Cria uma caixa de seleção na barra lateral. 
        colunaY = st.selectbox(
            "Eixo Y",
            options = ["umidade", "temperatura", "pressao", "altitude", "co2", "poeira", "tempo_registro"],
            index = 1,
            key='eixoy3'
        )
    
    if colunaX == colunaY:
        st.warning("Selecione uma opção diferente para os eixos X e Y")
        return
    try:
        cores_personalizadas = {'São Paulo': '#455354', 'Grande ABC': '#77A074'}
        fig_valores3 = px.scatter(
            df_selecionado, 
            x = colunaX, 
            y = colunaY,
            color='regiao',
            title=f"Gráfico de Dispersão por Região: {colunaX.capitalize()} vs {colunaY.capitalize()}",
            color_discrete_map = cores_personalizadas                        
            )  
        
        st.plotly_chart(fig_valores3, use_container_width=True)
            
    except Exception as e:
        st.error(f"Erro ao criar gráfico de dispersão: {e}")
        
def grafico_area(df_selecionado):
    # Seleção da coluna X  |  selectbox ==> Cria uma caixa de seleção na barra lateral. 
    with st.expander("Selecione os eixos"):
        colunaX = st.selectbox(
            "Eixo X",
            options = ["tempo_registro"],
            index = 0,
            key='eixox4'
        )

        # Seleção da coluna Y  |  selectbox ==> Cria uma caixa de seleção na barra lateral. 
        colunaY = st.selectbox(
            "Eixo Y",
            options = ["umidade", "temperatura", "pressao", "altitude", "co2", "poeira"],
            index = 1,
            key='eixoy4'
        )
    
    if colunaX == colunaY:
        st.warning("Selecione uma opção diferente para os eixos X e Y")
        return
    try:
        grupo_dados4 = df_selecionado.groupby(by=[colunaX]).size().reset_index(name=colunaY)
        st.area_chart(grupo_dados4, x = colunaX, y = colunaY, color= ["#455354"], stack="center" )

    except Exception as e:
        st.error(f"Erro ao criar gráfico de area: {e}")
        
def grafico_barrasEmpilhadas(df_selecionado):
    # Seleção da coluna X  |  selectbox ==> Cria uma caixa de seleção na barra lateral. 
    with st.expander("Selecione os eixos"): 
        colunaX = st.selectbox(
            "Eixo X",
            options = ["umidade", "temperatura", "pressao", "altitude", "co2", "poeira", "tempo_registro"],
            index = 0,
            key='eixox5'
        )

        # Seleção da coluna Y  |  selectbox ==> Cria uma caixa de seleção na barra lateral. 
        colunaY = st.selectbox(
            "Eixo Y",
            options = ["umidade", "temperatura", "pressao", "altitude", "co2", "poeira", "tempo_registro"],
            index = 1,
            key='eixoy5'
        )
    
    if colunaX == colunaY:
        st.warning("Selecione uma opção diferente para os eixos X e Y")
        return
    try:   
        cores_personalizadas = {
            'São Paulo': '#455354',  # Cor para a região Norte
            'Grande ABC': '#77A074'    # Cor para a região Sul
        }
    
        fig_barra = px.bar(df_selecionado, 
                            x=colunaX,
                            y=colunaY,
                            color='regiao',
                            barmode='group',
                            title='Gráfico de Barras Empilhadas por Região',
                            color_discrete_map= cores_personalizadas
                            )
        
        st.plotly_chart(fig_barra, use_container_width=True)
    
    except Exception as e:
        print(f'Erro ao criar o gráfico de barras empilhadas: {e}')
        
        
# *********************************SLIDERS *****************************

# Verificar quais os atributos do filtro. 
# def filtros(atributo):
#     return atributo in [colunaX, colunaY]

# # Filtro de RANGE ==> SLIDER
# st.sidebar.header("Selecione o filtro")

# # UMIDADE
# if filtros("umidade"):
#     umidade_range = st.sidebar.slider(
#         "Umidade",
#         min_value = float(df["umidade"].min()),  # Valor Mínimo.
#         max_value = float(df["umidade"].max()),  # Valor Máximo.
#         value = (float(df["umidade"].min()), float(df["umidade"].max())),  # Faixa de Valores selecionado.
#         step = 0.1   # Incremento para cada movimento do slider.  
#     )

# # TEMPERATURA
# if filtros("temperatura"):
#     temperatura_range = st.sidebar.slider(
#         "Temperatura (°C)",
#         min_value = float(df["temperatura"].min()),  # Valor Mínimo.
#         max_value = float(df["temperatura"].max()),  # Valor Máximo.
#         value = (float(df["temperatura"].min()), float(df["temperatura"].max())),  # Faixa de Valores selecionado.
#         step = 0.1   # Incremento para cada movimento do slider. 
#     )

# # PRESSÃO
# if filtros("pressao"):
#     pressao_range = st.sidebar.slider(
#         "Pressao",
#         min_value = float(df["pressao"].min()),  # Valor Mínimo.
#         max_value = float(df["pressao"].max()),  # Valor Máximo.
#         value = (float(df["pressao"].min()), float(df["pressao"].max())),  # Faixa de Valores selecionado.
#         step = 0.1   # Incremento para cada movimento do slider. 
#     )

# # ALTITUDE
# if filtros("altitude"):
#     altitude_range = st.sidebar.slider(
#         "Altitude",
#         min_value = float(df["altitude"].min()),  # Valor Mínimo.
#         max_value = float(df["altitude"].max()),  # Valor Máximo.
#         value = (float(df["altitude"].min()), float(df["altitude"].max())),  # Faixa de Valores selecionado.
#         step = 0.1   # Incremento para cada movimento do slider. 
#     )

# # CO2
# if filtros("co2"):
#     co2_range = st.sidebar.slider(
#         "CO2",
#         min_value = float(df["co2"].min()),  # Valor Mínimo.
#         max_value = float(df["co2"].max()),  # Valor Máximo.
#         value = (float(df["co2"].min()), float(df["co2"].max())),  # Faixa de Valores selecionado.
#         step = 0.1   # Incremento para cada movimento do slider. 
#     )

# # POEIRA
# if filtros("poeira"):
#     poeira_range = st.sidebar.slider(
#         "Poeira",
#         min_value = float(df["poeira"].min()),  # Valor Mínimo.
#         max_value = float(df["poeira"].max()),  # Valor Máximo.
#         value = (float(df["poeira"].min()), float(df["poeira"].max())),  # Faixa de Valores selecionado.
#         step = 0.1   # Incremento para cada movimento do slider. 
#     )
# ## ************************************ FILTROS TEMPO_REGISTRO *************************************
# if filtros("tempo_registro"):
#     # Extrair as datas mínimas e máximas em formato de datetime
#     min_data = df["tempo_registro"].min()
#     max_data = df["tempo_registro"].max()

#     # Exibir dois campos de data para seleção de intervalo no sidebar
#     data_inicio = st.sidebar.date_input(
#         "Data de Início", 
#         min_data.date(), 
#         min_value=min_data.date(), 
#         max_value=max_data.date(),
#         format= "DD-MM-YYYY"
#     )
    
#     data_fim = st.sidebar.date_input(
#         "Data de Fim", 
#         max_data.date(), 
#         min_value=min_data.date(), 
#         max_value=max_data.date(),
#         format= "DD-MM-YYYY"
#     )

#     # Converter as datas selecionadas para datetime, incluindo hora
#     tempo_registro_range = (
#         pd.to_datetime(data_inicio),
#         pd.to_datetime(data_fim) + pd.DateOffset(days=1) - pd.Timedelta(seconds=1)
#     )

# if filtros("umidade"):
#     df_selecionado = df_selecionado[
#         (df_selecionado["umidade"] >= umidade_range[0]) &
#         (df_selecionado["umidade"] <= umidade_range[1])
#     ]

# if filtros("temperatura"):
#     df_selecionado = df_selecionado[
#         (df_selecionado["temperatura"] >= temperatura_range[0]) &
#         (df_selecionado["temperatura"] <= temperatura_range[1])
#     ]

# if filtros("pressao"):
#     df_selecionado = df_selecionado[
#         (df_selecionado["pressao"] >= pressao_range[0]) &
#         (df_selecionado["pressao"] <= pressao_range[1])
#     ]
    
# if filtros("altitude"):
#     df_selecionado = df_selecionado[
#         (df_selecionado["altitude"] >= altitude_range[0]) &
#         (df_selecionado["altitude"] <= altitude_range[1])
#     ]

# if filtros("co2"):
#     df_selecionado = df_selecionado[
#         (df_selecionado["co2"] >= co2_range[0]) &
#         (df_selecionado["co2"] <= co2_range[1])
#     ]

# if filtros("poeira"):
#     df_selecionado = df_selecionado[
#         (df_selecionado["poeira"] >= poeira_range[0]) &
#         (df_selecionado["poeira"] <= poeira_range[1])
#     ] 

# if filtros("tempo_registro"):
#     df_selecionado = df_selecionado[
#         (df_selecionado["tempo_registro"] >= tempo_registro_range[0]) &
#         (df_selecionado["tempo_registro"] <= tempo_registro_range[1])
#     ] 