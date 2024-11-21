import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import *
from datetime import datetime
from streamlit_modal import Modal
import scipy.stats as stats
import plotly.graph_objects as go

def grafico_barras(df_selecionado):
    with st.expander("Selecione os eixos"): 
        colunaX = st.selectbox(
            "Eixo X",
            options=["tempo_registro"],
            index=0,
            key='eixox_barras'
        )

        colunaY = st.selectbox(
            "Eixo Y",
            options=["umidade", "temperatura", "pressao", "altitude", "co2", "poeira"],
            index=1,
            key='eixoy_barras'
        )

    if colunaX == colunaY:
        st.warning("Selecione uma opção diferente para os eixos X e Y")
        return

    with st.expander("Configuração de intervalo"):
        intervalo = st.selectbox(
            "Escolha o intervalo para calcular a média",
            options=["15T", "30T", "1H", "6H", "1D"],
            index=2,
            key="intervalo_barras"
        )

    try:
        # Agrupar e calcular a média por intervalo
        df_selecionado['tempo_registro'] = pd.to_datetime(df_selecionado['tempo_registro'])
        df_selecionado['tempo_alinhado'] = df_selecionado['tempo_registro'].dt.floor(intervalo)
        df_agrupado = df_selecionado.groupby(['regiao', 'tempo_alinhado'])[colunaY].mean().reset_index()

        # Gráfico de Barras
        cores_personalizadas = {'São Paulo': '#455354', 'Grande ABC': '#77A074'}
        fig_barras = px.bar(
            df_agrupado,
            x='tempo_alinhado',
            y=colunaY,
            color="regiao",
            title=f"Gráfico de Barras (Médias): {colunaX.capitalize()} vs {colunaY.capitalize()}",
            color_discrete_map=cores_personalizadas,
            template="plotly_white"
        )
        st.plotly_chart(fig_barras, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao criar gráfico de barras: {e}")
    
def grafico_linhas(df_selecionado):
    with st.expander("Selecione os eixos"):
        colunaX = st.selectbox(
            "Eixo X",
            options=["tempo_registro"],
            index=0,
            key='eixox_linhas'
        )

        colunaY = st.selectbox(
            "Eixo Y",
            options=["umidade", "temperatura", "pressao", "co2", "poeira"],
            index=1,
            key='eixoy_linhas'
        )
    
    if colunaX == colunaY:
        st.warning("Selecione uma opção diferente para os eixos X e Y")
        return
    
    # Seleção de intervalo de agrupamento
    with st.expander("Configuração de intervalo"):
        intervalo = st.selectbox(
            "Escolha o intervalo para calcular a média",
            options=["15T", "30T", "1H", "6H", "1D"],
            index=2,  # Default: 1 hora
            key="intervalo_medio"
        )

    try:
        # Converter a coluna de tempo para datetime
        df_selecionado['tempo_registro'] = pd.to_datetime(df_selecionado['tempo_registro'])
        
        # Agrupar por região e intervalo de tempo, calculando a média
        df_selecionado['tempo_alinhado'] = df_selecionado['tempo_registro'].dt.floor(intervalo)
        df_agrupado = df_selecionado.groupby(['regiao', 'tempo_alinhado'])[colunaY].mean().reset_index()

        # Gráfico com Plotly
        cores_personalizadas = {'São Paulo': '#455354', 'Grande ABC': '#77A074'}          
        fig_valores2 = px.line(
            df_agrupado,
            x='tempo_alinhado',
            y=colunaY,
            color="regiao",
            title=f"Gráfico de Linhas (Médias): {colunaX.capitalize()} vs {colunaY.capitalize()}",
            color_discrete_map=cores_personalizadas,
            line_shape='linear', 
            markers=True  # Mostrar marcadores nos pontos
        )
        
        # Configuração do layout do gráfico
        fig_valores2.update_layout(
            xaxis_title='Tempo (Intervalos Alinhados)',
            yaxis_title=f'{colunaY.capitalize()} Média',
            template='plotly_white'
        )
        
    except Exception as e:
        st.error(f"Erro ao criar gráfico de linhas: {e}")
        return
    
    # Exibir gráfico no Streamlit
    st.plotly_chart(fig_valores2, use_container_width=True)
    
def grafico_dispersao(df_selecionado):
    with st.expander("Selecione os eixos"):
        colunaX = st.selectbox(
            "Eixo X",
            options=["tempo_registro", "umidade", "temperatura", "pressao", "altitude", "co2", "poeira"],
            index=0,
            key='eixox_dispersao'
        )

        colunaY = st.selectbox(
            "Eixo Y",
            options=["umidade", "temperatura", "pressao", "altitude", "co2", "poeira"],
            index=1,
            key='eixoy_dispersao'
        )

    if colunaX == colunaY:
        st.warning("Selecione uma opção diferente para os eixos X e Y")
        return

    try:
        
        # Se a coluna X for 'tempo_registro', converta para um valor numérico (exemplo: número de dias)
        if colunaX == "tempo_registro":
            df_selecionado[colunaX] = (df_selecionado[colunaX] - df_selecionado[colunaX].min()).dt.total_seconds() / (60 * 60 * 24)  # dias
        # Se a coluna Y for 'tempo_registro', converta para um valor numérico (exemplo: número de dias)
        if colunaY == "tempo_registro":
            df_selecionado[colunaY] = (df_selecionado[colunaY] - df_selecionado[colunaY].min()).dt.total_seconds() / (60 * 60 * 24)  # dias      
        
        # Calcula a regressão linear
        x = df_selecionado[colunaX]
        y = df_selecionado[colunaY]
        
        # Realiza a regressão linear usando scipy
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Calcula a linha de regressão (y = mx + b)
        linha_regressao = slope * x + intercept
             
        cores_personalizadas = {'São Paulo': '#455354', 'Grande ABC': '#77A074'}
        fig_dispersao = px.scatter(
            df_selecionado,
            x=colunaX,
            y=colunaY,
            color="regiao",
            title=f"Gráfico de Dispersão: {colunaX.capitalize()} vs {colunaY.capitalize()}",
            color_discrete_map=cores_personalizadas,
            template="plotly_white"
        )
        
        # Adiciona a linha de regressão ao gráfico
        fig_dispersao.add_trace(
            go.Scatter(
                x=x,
                y=linha_regressao,
                mode='lines',
                name=f"Regressão Linear",
                line=dict(color='red', dash='dash')
            )
        )
        
        st.plotly_chart(fig_dispersao, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao criar gráfico de dispersão: {e}")
        
def grafico_area(df_selecionado):
    with st.expander("Selecione os eixos"):
        colunaX = st.selectbox(
            "Eixo X",
            options=["tempo_registro"],
            index=0,
            key='eixox_area'
        )

        colunaY = st.selectbox(
            "Eixo Y",
            options=["umidade", "temperatura", "pressao", "altitude", "co2", "poeira"],
            index=1,
            key='eixoy_area'
        )

    if colunaX == colunaY:
        st.warning("Selecione uma opção diferente para os eixos X e Y")
        return

    with st.expander("Configuração de intervalo"):
        intervalo = st.selectbox(
            "Escolha o intervalo para calcular a soma",
            options=["15T", "30T", "1H", "6H", "1D"],
            index=2,
            key="intervalo_area"
        )

    try:
        df_selecionado['tempo_registro'] = pd.to_datetime(df_selecionado['tempo_registro'])
        df_selecionado['tempo_alinhado'] = df_selecionado['tempo_registro'].dt.floor(intervalo)
        df_agrupado = df_selecionado.groupby(['tempo_alinhado', 'regiao'])[colunaY].sum().reset_index()

        # Gráfico de Área
        cores_personalizadas = {'São Paulo': '#455354', 'Grande ABC': '#77A074'}
        fig_area = px.area(
            df_agrupado,
            x='tempo_alinhado',
            y=colunaY,
            color="regiao",
            title=f"Gráfico de Área (Somas): {colunaX.capitalize()} vs {colunaY.capitalize()}",
            color_discrete_map=cores_personalizadas,
            template="plotly_white"
        )
        st.plotly_chart(fig_area, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao criar gráfico de área: {e}")
        
def grafico_barras_empilhadas(df_selecionado):
    with st.expander("Selecione os eixos"):
        colunaX = st.selectbox(
            "Eixo X",
            options=["tempo_registro", "umidade", "temperatura", "pressao", "altitude", "co2", "poeira"],
            index=0,
            key='eixox_empilhadas'
        )

        colunaY = st.selectbox(
            "Eixo Y",
            options=["umidade", "temperatura", "pressao", "altitude", "co2", "poeira"],
            index=1,
            key='eixoy_empilhadas'
        )

    if colunaX == colunaY:
        st.warning("Selecione uma opção diferente para os eixos X e Y")
        return

    with st.expander("Configuração de intervalo"):
        intervalo = st.selectbox(
            "Escolha o intervalo para calcular a soma",
            options=["15T", "30T", "1H", "6H", "1D"],
            index=2,
            key="intervalo_empilhadas"
        )

    try:
        df_selecionado['tempo_registro'] = pd.to_datetime(df_selecionado['tempo_registro'])
        df_selecionado['tempo_alinhado'] = df_selecionado['tempo_registro'].dt.floor(intervalo)
        df_agrupado = df_selecionado.groupby(['tempo_alinhado', 'regiao'])[colunaY].sum().reset_index()

        # Gráfico de Barras Empilhadas
        cores_personalizadas = {'São Paulo': '#455354', 'Grande ABC': '#77A074'}
        fig_empilhadas = px.bar(
            df_agrupado,
            x='tempo_alinhado',
            y=colunaY,
            color="regiao",
            barmode='stack',
            title=f"Gráfico de Barras Empilhadas (Somas): {colunaX.capitalize()} vs {colunaY.capitalize()}",
            color_discrete_map=cores_personalizadas,
            template="plotly_white"
        )
        st.plotly_chart(fig_empilhadas, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao criar gráfico de barras empilhadas: {e}")
        
        
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