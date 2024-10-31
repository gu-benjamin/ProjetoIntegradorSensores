import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import *
from datetime import datetime

from Projeto_Integrador.Projeto_Integrador_Completo.query import conexao

query = "SELECT * FROM tb_registro"  # Consulta com o banco de dados.

df = conexao(query)                  # Carregar os dados do MySQL.

if st.button("Atualizar dados"):     # Botão para atualização dos dados.
    df = conexao(query)

df['tempo_registro'] = pd.to_datetime(df['tempo_registro'])  # Converter para datetime
# ****************************** MENU LATERAL ******************************
st.sidebar.header("Selecione a informação para gerar o gráfico")  

# Seleção da coluna X  |  selectbox ==> Cria uma caixa de seleção na barra lateral. 
colunaX = st.sidebar.selectbox(
    "Eixo X",
    options = ["umidade", "temperatura", "pressao", "altitude", "co2", "poeira", "tempo_registro"],
    index = 0
)

# Seleção da coluna Y  |  selectbox ==> Cria uma caixa de seleção na barra lateral. 
colunaY = st.sidebar.selectbox(
    "Eixo Y",
    options = ["umidade", "temperatura", "pressao", "altitude", "co2", "poeira", "tempo_registro"],
    index = 1
)

# Verificar quais os atributos do filtro. 
def filtros(atributo):
    return atributo in [colunaX, colunaY]

# Filtro de RANGE ==> SLIDER
st.sidebar.header("Selecione o filtro")

# UMIDADE
if filtros("umidade"):
    umidade_range = st.sidebar.slider(
        "Umidade",
        min_value = float(df["umidade"].min()),  # Valor Mínimo.
        max_value = float(df["umidade"].max()),  # Valor Máximo.
        value = (float(df["umidade"].min()), float(df["umidade"].max())),  # Faixa de Valores selecionado.
        step = 0.1   # Incremento para cada movimento do slider.  
    )

# TEMPERATURA
if filtros("temperatura"):
    temperatura_range = st.sidebar.slider(
        "Temperatura (°C)",
        min_value = float(df["temperatura"].min()),  # Valor Mínimo.
        max_value = float(df["temperatura"].max()),  # Valor Máximo.
        value = (float(df["temperatura"].min()), float(df["temperatura"].max())),  # Faixa de Valores selecionado.
        step = 0.1   # Incremento para cada movimento do slider. 
    )

# PRESSÃO
if filtros("pressao"):
    pressao_range = st.sidebar.slider(
        "Pressao",
        min_value = float(df["pressao"].min()),  # Valor Mínimo.
        max_value = float(df["pressao"].max()),  # Valor Máximo.
        value = (float(df["pressao"].min()), float(df["pressao"].max())),  # Faixa de Valores selecionado.
        step = 0.1   # Incremento para cada movimento do slider. 
    )

# ALTITUDE
if filtros("altitude"):
    altitude_range = st.sidebar.slider(
        "Altitude",
        min_value = float(df["altitude"].min()),  # Valor Mínimo.
        max_value = float(df["altitude"].max()),  # Valor Máximo.
        value = (float(df["altitude"].min()), float(df["altitude"].max())),  # Faixa de Valores selecionado.
        step = 0.1   # Incremento para cada movimento do slider. 
    )

# CO2
if filtros("co2"):
    co2_range = st.sidebar.slider(
        "CO2",
        min_value = float(df["co2"].min()),  # Valor Mínimo.
        max_value = float(df["co2"].max()),  # Valor Máximo.
        value = (float(df["co2"].min()), float(df["co2"].max())),  # Faixa de Valores selecionado.
        step = 0.1   # Incremento para cada movimento do slider. 
    )

# POEIRA
if filtros("poeira"):
    poeira_range = st.sidebar.slider(
        "Poeira",
        min_value = float(df["poeira"].min()),  # Valor Mínimo.
        max_value = float(df["poeira"].max()),  # Valor Máximo.
        value = (float(df["poeira"].min()), float(df["poeira"].max())),  # Faixa de Valores selecionado.
        step = 0.1   # Incremento para cada movimento do slider. 
    )
# Tempo Registro
if filtros("tempo_registro"):
    # Converter os valores mínimo e máximo para timestamp
    min_timestamp = df["tempo_registro"].min().timestamp()
    max_timestamp = df["tempo_registro"].max().timestamp()
    
    tempo_registro_range = st.sidebar.slider(
        "Tempo Registro",
        min_value=min_timestamp,  # Valor Mínimo como timestamp.
        max_value=max_timestamp,  # Valor Máximo como timestamp.
        value=(min_timestamp, max_timestamp),  # Faixa de Valores selecionado.
        format="DD-MM-YY - hh:mm"  # Formato de exibição (não vai afetar a seleção)
    )
    # Converter o range de volta para datetime
    tempo_registro_range = (pd.to_datetime(tempo_registro_range[0], unit='s'),
                            pd.to_datetime(tempo_registro_range[1], unit='s'))
# Região
if filtros("regiao"):
    regiao_range = st.sidebar.slider(
        "regiao",
        min_value = float(df["regiao"].min()),  # Valor Mínimo.
        max_value = float(df["regiao"].max()),  # Valor Máximo.
        value = (float(df["regiao"].min()), (df["regiao"].max())),  # Faixa de Valores selecionado.
        step = 0.1   # Incremento para cada movimento do slider. 
    )


df_selecionado = df.copy()   # Cria uma copia do df original.:


if filtros("umidade"):
    df_selecionado = df_selecionado[
        (df_selecionado["umidade"] >= umidade_range[0]) &
        (df_selecionado["umidade"] <= umidade_range[1])
    ]

if filtros("temperatura"):
    df_selecionado = df_selecionado[
        (df_selecionado["temperatura"] >= temperatura_range[0]) &
        (df_selecionado["temperatura"] <= temperatura_range[1])
    ]

if filtros("pressao"):
    df_selecionado = df_selecionado[
        (df_selecionado["pressao"] >= pressao_range[0]) &
        (df_selecionado["pressao"] <= pressao_range[1])
    ]
    
if filtros("altitude"):
    df_selecionado = df_selecionado[
        (df_selecionado["altitude"] >= altitude_range[0]) &
        (df_selecionado["altitude"] <= altitude_range[1])
    ]

if filtros("co2"):
    df_selecionado = df_selecionado[
        (df_selecionado["co2"] >= co2_range[0]) &
        (df_selecionado["co2"] <= co2_range[1])
    ]

if filtros("poeira"):
    df_selecionado = df_selecionado[
        (df_selecionado["poeira"] >= poeira_range[0]) &
        (df_selecionado["poeira"] <= poeira_range[1])
    ] 

if filtros("tempo_registro"):
    df_selecionado = df_selecionado[
        (df_selecionado["tempo_registro"] >= tempo_registro_range[0]) &
        (df_selecionado["tempo_registro"] <= tempo_registro_range[1])
    ] 
    

    
# **************************** GRÁFICOS ****************************

def Home():
    with st.expander("Tabela"):
        mostrarDados = st.multiselect(
            "Filtro: ",
            df_selecionado.columns,
            default=[],
            key = "showData_home"
        )
        
        if mostrarDados:
            st.write(df_selecionado[mostrarDados])
    
    # Cálculos estatísticos
    if not df_selecionado.empty:
        media_umidade = df_selecionado["umidade"].mean()
        media_temperatura = df_selecionado["temperatura"].mean()
        media_co2 = df_selecionado["co2"].mean()\
        
        media1, media2, media3 = st.columns(3, gap="large")
        
        with media1: 
            st.info("Média de registros de Umidade", icon="📌")
            st.metric(label="Média", value=f"{media_umidade:.2f}")
        
        with media2:
            st.info("Média de registros de Temperatura (°C)", icon="📌")
            st.metric(label="Média", value=f"{media_temperatura:.2f}")
        
        with media3:
            st.info("Média de registros de CO2", icon="📌")
            st.metric(label="Média", value=f"{media_co2:.2f}")

# **************************** PLOTANDO GRÁFICOS ****************************
def graficos():
    st.title("Dashboard Monitoramento")
       
    aba1, aba2, aba3, aba4, aba5  = st.tabs(
        ["Gráfico de Barras",
        "Gráfico de Linhas",
        "Gráfico de Dispersão",
        "Gráfico de Área",
        "Gráfico de ----"]
        )
    
    with aba1:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar gráficos")
            return
        
        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return
        
        try:           
            grupo_dados1 = df_selecionado.groupby(by=[colunaX]).size().reset_index(name="contagem")
            fig_valores = px.bar(
                grupo_dados1,       # De onde vem os dados.
                x = colunaX,        # Eixo X
                y = "contagem",     # Eixo Y com o nome que nós renomeamos no GrupBy
                orientation = "v",  # Orientação do Gráfico
                title = f"Contagem de Registros por {colunaX.capitalize()}", # Titulo do gráfico => A função capitalize() deixa tudo em maiúsculo. 
                color_discrete_sequence = ["#0083b8"],       # Altera a cor 
                template = "plotly_white"
            )
            
        except Exception as e:
            st.error(f"Erro ao criar gráfico de barras:  {e}")
        st.plotly_chart(fig_valores, use_container_width=True)

    with aba2:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar gráficos")
            return

        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return

        try:
            grupo_dados2 = df_selecionado.groupby(by=[colunaX])[colunaY].mean().reset_index(name=colunaY)
            fig_valores2 = px.line(
                grupo_dados2,
                x=colunaX,
                y=colunaY,
                title=f"Gráfico de Linhas: {colunaX.capitalize()} vs {colunaY.capitalize()}",
                line_shape='linear',  # Tipo de linha
                markers=True  # Para mostrar marcadores nos pontos
            )
        except Exception as e:
            st.error(f"Erro ao criar gráfico de linhas: {e}")
        st.plotly_chart(fig_valores2, use_container_width=True)
 
    with aba3:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar gráficos")
            return

        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return

        try:
            grupo_dados3 = df_selecionado.groupby(by=[colunaX]).size().reset_index(name=colunaY)
            fig_valores3 = px.scatter(grupo_dados3, x = colunaX, y = colunaY)    
            
            st.plotly_chart(fig_valores3, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao criar gráfico de disperção: {e}")
    
    with aba4:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar gráficos")
            return
        
        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return
        
        try:
            grupo_dados4 = df_selecionado.groupby(by=[colunaX]).size().reset_index(name=colunaY)
            st.area_chart(grupo_dados4, x = colunaX, y = colunaY, color= ["#0083b8"], stack="center" )

        except Exception as e:
            st.error(f"Erro ao criar gráfico de dispersão: {e}")
        
    with aba5:
        if df_selecionado.empty:
            st.write('Nenhum dado está disponível para gerar o gráfico')
            return
        
        if colunaX == colunaY:
            st.warning('Selecione uma opção diferente para os eixos X e Y')
            return
        
        try:
            grupo_dados5 = df_selecionado
            fig_barra = px.bar(grupo_dados5, 
                               x=colunaX,
                               y=colunaY,
                               color='regiao',
                               barmode='group',
                               title='Comparação entre regiões'
                               )
            
            st.plotly_chart(fig_barra, use_container_width=True)
            
        except Exception as e:
            print(f'Erro ao criar o gráfico: {e}')
# **************************** CHAMANDO A FUNÇÃO ****************************
Home()
graficos()